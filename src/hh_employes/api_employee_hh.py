from pydantic import ConfigDict, HttpUrl, Field
from typing import Any, Union, ClassVar, Dict, List, Type

from queue import Queue
from src.utils.correct_tuple import CorrectValues
import httpx
import asyncio
from src.abstract.abstract_classes import AbstractApi
from src.hh_employes.employeer import Employeers
from src.hh_vacancies.api_hh import HhVacancies
from src.hh_vacancies.vacancies import Vacancy


class HhEmpoloyee(AbstractApi):
    
    model_config = ConfigDict(frozen=True)
    
    __url: ClassVar[HttpUrl] = 'https://api.hh.ru/employers'
    _response: ClassVar[Union[dict, None]] = None
    
    name: Union[str, None] = Field(max_length=30)
    per_page: Union[int, None] = Field(ge=0, default=10)
    page: Union[int, None] = Field(ge=0, default=0)
    session: Any
    
     
    @property
    async def response(self) -> Dict:
        """Возращает готовый и обработанный запрос
        """  
        await self._build_response(self.session)  
        return self._response
    
    
    async def _build_response(self, session) -> List[Dict]:
        """Метод отправки запроса
        """
        result = await session.get(url=self.__url, params=self._make_params())
        HhEmpoloyee._response = result.json()
    
    
    def _make_params(self):
        """метод который собирает параметры для запроса
        """  
              
        params = {
            'text': self.name,
            'per_page': self.per_page,
            'page': self.page,
            'only_with_vacancies': True,
            'sort_by': 'by_vacancies_open'
            
        }
        
        return params
