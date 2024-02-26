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
    """Апи который отвечает за перевод иностранной валюты

    Returns:
        dict: Возвращает ответ с индексами необходимых иностранных валют
    """    
    
    __url: ClassVar[HttpUrl] = 'https://api.apilayer.com/exchangerates_data/latest?'
    __api: ClassVar[str] = os.environ.get('API_EXCHANGE')
    __base :ClassVar[str] = 'RUB'
    __ex_change: ClassVar[Union[Dict, None]] = None
    
    symbols: List
    
    def model_post_init(self, __context: Any) -> None:
        ApiChange.ex_change = self._build_response()
    
    @property
    def ex_change(self) -> Dict:
        return self.__ex_change
    
    def _make_params(self):
        """Параметры для запроса (почему то не работает, сделал в ручную)
        """   
             
        params = {      
          'symbol': self.symbols,
          'base': self.__base
        }
        
        return params
      
    def _make_header(self):
        """Заголовок для запроса
        """   
             
        header = {
        'apikey': self.__api
        }
      
        return header
    
    def _build_response(self) -> Dict:
        """Построение запроса исходя из всех полученных параметров

        Returns:
            Dict: Возращает ответ от сокета сервера
        """
                
        requests_api = requests.request('GET', f'{self.__url}symbols={'%2C%20'.join(self.symbols)}\
            &base={self.__base}', headers=self._make_header())
        response = requests_api.json()
        
        return response


class MixinConvert(BaseModel, extra='allow'):
    """Миксин для внедрения Exchange в основную программу
    """   
     
    convert_to_RUB: bool = False
    
    def _make_list_for_convert(self, list_: List[Dict]):
        """Метод который проходится по списку объектов и выводит иностранные валюты

        Args:
            list_ (List[Dict]): Список с объектами
        """  
              
        currencies = []
        
        [currencies.append(item['salary']['currency']) 
         for item in list_
         if item['salary']['currency'] != 'RUR' and item['salary']['currency'] not in currencies]
        
        return currencies
    
    def get_rate_currency(self, list_: List[str]) -> Dict:
        """API которое получает список валют которые войдут в запрос

        Args:
            list_ (List[str]): Список валют

        Returns:
            Dict: Возращает результат запроса с индексами указанных валют
        """ 
               
        rates = ApiChange(symbols=list_)
        
        if rates.ex_change.get('rates'):
            return rates.ex_change

    def _convert_valute(self, list_: List[Dict]) -> List[Dict]:
        """Метод который проходится по списку с объетами и меняет 
        значение денежного эквивалетна у тех у котого иностранная валюта

        Args:
            list_ (List[Dict]): Список до конвертации

        Returns:
            List[Dict]: Список после конвертации
        """    
            
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
    """Миксин сортировки объектов по определенному значению
    """    
    
    def __init_subclass__(cls, **kwargs: ConfigDict):
        return super().__init_subclass__(**kwargs)
        
    def _sort_json_response(self, dict_: List[Dict]) -> List[Dict]:
        """Сортировка JSON файла по зарплате

        Returns:
            Dict: Возращает отсортированный словарь
        """  
              
        sorted_json = sorted(dict_, key=lambda x: x['salary']['from'], reverse=True)
        
        HhVacancies._response = sorted_json
    

class MixinTown(BaseModel, extra='allow'):
    """Миксин итеграции функциональности поиска по определенному городу
    """    
    
    def __init_subclass__(cls, **kwargs: ConfigDict):
        return super().__init_subclass__(**kwargs)
    town: Union[str, None] = None
    
    def make_id_of_town(self, town: str) -> int:
        """Метод получает имя города и возразает ID

        Args:
            town (str): имя города

        Returns:
            int: ID города
        """  
           
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
        """Метод пост-инициализации, меняет состояние выходящего запроса
        исходя из параметров
        """   
             
        self._build_response()
        if self.convert_to_RUB:
            self._convert_valute(self._response)
        self._sort_json_response(self._response)
        
        
    @field_validator('town')
    @classmethod
    def town(cls, value: Union[str, None]) -> Union[str, None]:
        """Валидация параметра город
        """  
              
        if value is None:
            return None
        
        value = value.replace('-', '').replace(' ', '').lower().title()
        if value not in [item.name for item in EnumTown]:
            return None
        
        return value
         
    @property
    def response(self) -> Dict:
        """Возращает готовый и обработанный запрос
        """    
            
        return self._response
    
    def _remove_null_instanse(self, list_: List[Dict]):
        """Метод переработки объектов в запросе и замена None на 0 в salary

        Args:
            list_ (List[Dict]): Список до обработки
        """        
        ready_list = list_
        
        for item in ready_list:
            if item['salary']['from'] is None:
                item['salary']['from'] = 0
                
        return ready_list
    
    def _build_response(self) -> List[Dict]:
        """Метод отправки запроса
        """ 
               
        request_api = requests.request('GET', self.__url, params=self._make_params())
        
        HhVacancies._response = self._remove_null_instanse(request_api.json()['items'])
    
    def _make_params(self):
        """метод который собирает параметры для запроса
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
