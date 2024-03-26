from pydantic import ConfigDict, HttpUrl, Field
from typing import Any, Union, ClassVar, Dict, List
from httpx import AsyncClient

from src.abstract.abstract_classes import AbstractApi


class HhEmpoloyee(AbstractApi):
    """Модель асинхронного запроса работадателя по имени
    """    
    
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
    
    
    async def _build_response(self, session: AsyncClient) -> List[Dict]:
        """Метод отправки запроса
        """
        
        result = await session.get(url=self.__url, params=self._make_params())
        HhEmpoloyee._response = result.json()
    
    
    def _make_params(self) -> Dict:
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
