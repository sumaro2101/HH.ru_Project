from pprint import pprint
import requests
from pydantic import BaseModel, ConfigDict, HttpUrl, Field
from typing import Any, Union, ClassVar, Dict
from abc import ABC, abstractmethod

class ApiHh(BaseModel, ABC):
    """Абстрактный класс API модели
    """  
      
    name: str
    per_page: int 
    page: int
    
    @abstractmethod
    def _make_params(self):
        pass
    
    @abstractmethod
    def _build_response(self):
        pass


class HhVacancies(ApiHh):
    """API модель запроса вакансии
    """    
    model_config = ConfigDict(frozen=True)
        
    __url: ClassVar[HttpUrl] = 'https://api.hh.ru/vacancies'
    __response : ClassVar[Union[dict, None]] = None
    
    name: str = Field(max_length=20)
    per_page: int = Field(ge=0, default=10)
    page: int = Field(ge=0, default=20)
    

    def model_post_init(self, __context: Any) -> None:
        HhVacancies.response = self._sort_json_response()
        
        
    @property
    def response(self) -> Dict:
        """Возращает готовый и обработанный запрос
        """        
        return self.__response


    def _sort_json_response(self) -> Dict:
        """Сортировка JSON файла по зарплате

        Raises:
            TypeError: Если страница не существует 

        Returns:
            Dict: Возращает осотрированный словарь
        """  
              
        try:
            sorted_json = sorted(self._build_response()['items'], key=lambda x: x['salary']['from'], reverse=True)
            
        except TypeError:
            raise TypeError('К сожалению такой страницы не существует, попробуйте выбрать другую (page)')
        
        return sorted_json
    
    
    def _build_response(self) -> Dict:
        """Отправка запроса
        """ 
               
        request_api = requests.request('GET', self.__url, params=self._make_params())
        
        return request_api.json()
    
    
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
