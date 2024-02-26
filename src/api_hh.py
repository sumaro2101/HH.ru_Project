import requests
import os
from pydantic import BaseModel, ConfigDict, HttpUrl, Field, field_validator
from typing import Any, Union, ClassVar, Dict, List
from abc import ABC, abstractmethod

from src.enum_town import EnumTown

class AbstractApi(BaseModel, ABC):
    """Абстрактный класс API модели
    """  
    
    @abstractmethod
    def _make_params(self):
        pass
    
    @abstractmethod
    def _build_response(self):
        pass


class ApiChange(AbstractApi):
    
    __url: ClassVar[HttpUrl] = 'https://api.apilayer.com/exchangerates_data/latest?'
    __api: ClassVar[str] = os.environ.get('API_EXCHANGE')
    __base :ClassVar[str] = 'RUB'
    __ex_change: ClassVar[Union[Dict, None]] = None
    
    symbols: List
    
    def model_post_init(self, __context: Any) -> None:
       ApiChange.ex_change = self._build_response()
    
    @property
    def ex_change(self):
      return self.__ex_change
    
    def _make_params(self):
        params = {      
          'symbol': self.symbols,
          'base': self.__base
        }
        
        return params
      
    def _make_header(self):
      header = {
        'apikey': self.__api
      }
      
      return header
    
    def _build_response(self):
      requests_api = requests.request('GET', f'{self.__url}symbols={'%2C%20'.join(self.symbols)}\
        &base={self.__base}', headers=self._make_header())
      response = requests_api.json()
      
      return response


class MixinConvert(BaseModel, extra='allow'):
    
    convert_to_RUB: bool = False
    
    def _make_list_for_convert(self, list_):
        currencies = []
        [currencies.append(item['salary']['currency']) 
         for item in list_
         if item['salary']['currency'] != 'RUR' and item['salary']['currency'] not in currencies]
        
        return currencies
    
    def get_rate_currency(self, list_):
        rates = ApiChange(symbols=list_)
        if rates.ex_change.get('rates'):
            return rates.ex_change

    def _convert_valute(self, list_):
        converted = list_
        if self.get_rate_currency(self._make_list_for_convert(list_)):
            for item in converted:
                if item['salary']['currency'] != 'RUR':
                    valute_item = item['salary']['from']
                    valute_rate = self.get_rate_currency(self._make_list_for_convert(list_))[item['salary']['currency']]
                    
                    item['salary']['from'] = int(valute_item / valute_rate)
                    if item['salary']['to']:
                        item['salary']['to'] = int(valute_item / valute_rate)
                    
        HhVacancies._response = converted


class MixinSort(BaseModel, extra='allow'):
    
    def __init_subclass__(cls, **kwargs: ConfigDict):
        return super().__init_subclass__(**kwargs)
        
    def _sort_json_response(self, dict_) -> Dict:
        """Сортировка JSON файла по зарплате

        Raises:
            TypeError: Если страница не существует 

        Returns:
            Dict: Возращает осотрированный словарь
        """  
              
        sorted_json = sorted(dict_, key=lambda x: x['salary']['from'], reverse=True)
        
        HhVacancies._response = sorted_json
    

class MixinTown(BaseModel, extra='allow'):
    
    def __init_subclass__(cls, **kwargs: ConfigDict):
        return super().__init_subclass__(**kwargs)
    town: Union[str, None] = None
    
    def make_id_of_town(self, town):
        if town is not None:
            return EnumTown[town].value


class HhVacancies(MixinTown ,MixinSort, MixinConvert, AbstractApi):
    """API модель запроса вакансии
    """    
    model_config = ConfigDict(frozen=True)
        
    __url: ClassVar[HttpUrl] = 'https://api.hh.ru/vacancies'
    _response : ClassVar[Union[dict, None]] = None
    
    def __init_subclass__(cls, **kwargs: ConfigDict):
        return super().__init_subclass__(**kwargs)
    name: Union[str, None] = Field(max_length=20)
    per_page: Union[int, None] = Field(ge=0, default=10)
    page: Union[int, None] = Field(ge=0, default=0)

    def model_post_init(self, __context: Any) -> None:
        self._build_response()
        if self.convert_to_RUB:
            self._convert_valute(self._response)
        self._sort_json_response(self._response)
        
        
    @field_validator('town')
    @classmethod
    def town(cls, value):
        if value is None:
            return None
        
        value = value.replace('-', '').replace(' ', '').lower().title()
        if value not in [item.name for item in EnumTown]:
            raise ValueError
        
        return value
         
    @property
    def response(self) -> Dict:
        """Возращает готовый и обработанный запрос
        """        
        return self._response
    
    def _remove_null_instanse(self, list_):
        ready_list = list_
        for item in ready_list:
            if item['salary']['from'] is None:
                item['salary']['from'] = 0
        return ready_list
    
    def _build_response(self) -> Dict:
        """Отправка запроса
        """ 
               
        request_api = requests.request('GET', self.__url, params=self._make_params())
        
        HhVacancies._response = self._remove_null_instanse(request_api.json()['items'])
    
    def _make_params(self) -> Dict:
        """Собирает параметры для запроса
        """        
        params = {
            'text': self.name,
            'per_page': self.per_page,
            'page': self.page,
            'only_with_salary': True,
            'area': self.make_id_of_town(self.town),
            'clusters': True
        }
        return params

