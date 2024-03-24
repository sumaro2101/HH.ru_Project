import requests
import os
from pydantic import HttpUrl
from typing import Any, Union, ClassVar, Dict, List

from src.abstract.abstract_classes import AbstractApi


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
        
        if requests_api.status_code != 200:
            return None
        
        return response
