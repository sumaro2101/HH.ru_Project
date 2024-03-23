import requests
from pydantic import ConfigDict, HttpUrl, Field, field_validator
from typing import Any, Union, ClassVar, Dict, List

from src.utils.enum_town import EnumTown
from src.mixins.mixins import MixinConvert, MixinSort, MixinTown
from src.abstract.abstract_classes import AbstractApi


class HhVacancies(MixinTown ,MixinSort, MixinConvert, AbstractApi):
    """API модель запроса вакансии
    """  
      
    model_config = ConfigDict(frozen=True)
        
    __url: ClassVar[HttpUrl] = 'https://api.hh.ru/vacancies'
    _response : ClassVar[Union[dict, None]] = None
    
    def __init_subclass__(cls, **kwargs: ConfigDict):
        return super().__init_subclass__(**kwargs)
    name: Union[str, None] = Field(max_length=20, default=None)
    per_page: Union[int, None] = Field(ge=0, default=10)
    page: Union[int, None] = Field(ge=0, default=0)
    employer_id: Union[int, List[int], None] = None

    def model_post_init(self, __context: Any) -> None:
        """Метод пост-инициализации, меняет состояние выходящего запроса
        исходя из параметров
        """   
             
        self._build_response()
        if self.convert_to_RUB:
            self._convert_valute(HhVacancies ,self._response)
        self._sort_json_response(HhVacancies, self._response)
        
        
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
            'employer_id': self.employer_id,
            'per_page': self.per_page,
            'page': self.page,
            'only_with_salary': True,
            'area': self.make_id_of_town(self.town),
            'clusters': True
        }
        return params
