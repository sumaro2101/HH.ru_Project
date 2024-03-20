import requests
from pydantic import ConfigDict, HttpUrl, Field
from typing import Any, Union, ClassVar, Dict, List

from src.mixins.mixins import MixinTown
from src.abstract.abstract_classes import AbstractApi

class HhEmpoloyee(MixinTown, AbstractApi):
    
    model_config = ConfigDict(frozen=True)
    
    __url: ClassVar[HttpUrl] = 'https://api.hh.ru/employers'
    _response: ClassVar[Union[dict, None]] = None
    
    def __init_subclass__(cls, **kwargs: ConfigDict):
        return super().__init_subclass__(**kwargs)
    name: Union[str, None] = Field(max_length=30)
    per_page: Union[int, None] = Field(ge=0, default=10)
    page: Union[int, None] = Field(ge=0, default=0)
    
    
    def model_post_init(self, __context: Any) -> None:
        self._build_response()
        
        
    @property
    def response(self) -> Dict:
        """Возращает готовый и обработанный запрос
        """    
            
        return self._response
    
    
    def _build_response(self) -> List[Dict]:
        """Метод отправки запроса
        """ 
               
        request_api = requests.request('GET', self.__url, params=self._make_params())
        
        HhEmpoloyee._response = request_api.json()
    
    
    def _make_params(self):
        """метод который собирает параметры для запроса
        """  
              
        params = {
            'text': self.name,
            'per_page': self.per_page,
            'page': self.page,
            'only_with_vacancies': True,
            'area': self.make_id_of_town(self.town),
            'sort_by': 'by_vacancies_open'
            
        }
        
        return params


a = HhEmpoloyee(name='Bell Integrator', page=0, per_page=10)
print(a.response['items'])
company = ['kt.team', 'Bell Integrator', 'НИИ Вектор', 'Компэл', 'FINAMP', 'Лаборатория Наносемантика', 'Тензор', 'Соломон', 'the_covert', 'На_Полке']
# "vacancy_search_fields": [
# {
# "id": "name",
# "name": "в названии вакансии"
# },
# {
# "id": "company_name",
# "name": "в названии компании"
# },
# {
# "id": "description",
# "name": "в описании вакансии"
# }
# ],