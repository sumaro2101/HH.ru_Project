import requests
import os
from pydantic import BaseModel, ConfigDict, HttpUrl, Field
from typing import Any, Union, ClassVar, Dict, List
from abc import ABC, abstractmethod


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
       ApiChange.ex_change = self._build_response()['rates']
    
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


class MixinConvert:
    
    def _make_list_for_convert(self):
        currencies = []
        [currencies.append(item['salary']['currency']) 
         for item in self._response 
         if item['salary']['currency'] != 'RUR' and item['salary']['currency'] not in currencies]
        
        return currencies
    
    def get_rate_currency(self, list):
        rates = ApiChange(symbols=list)
        
        return rates.ex_change

    def _convert_valute(self):
        converted = self._response
        for item in converted:
            if item['salary']['currency'] != 'RUR':
                valute_item = item['salary']['from']
                valute_rate = self.get_rate_currency(self._make_list_for_convert())[item['salary']['currency']]
                
                item['salary']['from'] = int(valute_item / valute_rate)
                if item['salary']['to']:
                    item['salary']['to'] = int(valute_item / valute_rate)
                    
        return converted


class MixinSort:
        
    def _sort_json_response(self) -> Dict:
        """Сортировка JSON файла по зарплате

        Raises:
            TypeError: Если страница не существует 

        Returns:
            Dict: Возращает осотрированный словарь
        """  
              
        try:
            sorted_json = sorted(self._response, key=lambda x: x['salary']['from'], reverse=True)
            
        except TypeError:
            raise TypeError('К сожалению такой страницы не существует, попробуйте выбрать другую (page)')
        
        return sorted_json
    

class HhVacancies(MixinSort, MixinConvert, AbstractApi):
    """API модель запроса вакансии
    """    
    model_config = ConfigDict(frozen=True)
        
    __url: ClassVar[HttpUrl] = 'https://api.hh.ru/vacancies'
    _response : ClassVar[Union[dict, None]] = None
    
    name: str = Field(max_length=20)
    per_page: int = Field(ge=0, default=10)
    page: int = Field(ge=0, default=20)
    convert_to_RUB: bool = False
    

    def model_post_init(self, __context: Any) -> None:
        self._build_response()
        if self.convert_to_RUB:
            self._convert_valute()
        self._sort_json_response()
         
    @property
    def response(self) -> Dict:
        """Возращает готовый и обработанный запрос
        """        
        return self._response
    
    def _build_response(self) -> Dict:
        """Отправка запроса
        """ 
               
        request_api = requests.request('GET', self.__url, params=self._make_params())
        
        HhVacancies._response = request_api.json()['items']
    
    def _make_params(self) -> Dict:
        """Собирает параметры для запроса
        """        
        params = {
            'text': self.name,
            'per_page': self.per_page,
            'page': self.page,
            'only_with_salary': True
            
        }
        return params
