from abc import ABC, abstractmethod
from pydantic import BaseModel, HttpUrl
from typing import Dict, List

class AbstractApi(BaseModel, ABC):
    """Абстрактный класс API модели
    """  
    
    @abstractmethod
    def _make_params(self):
        pass
    
    @abstractmethod
    def _build_response(self):
        pass
    
    
class AbstractVacancies(BaseModel, ABC):
    
    name: str
    area: Dict
    professional_roles: List
    salary: Dict
    experience: Dict
    employment: Dict
    schedule: Dict
    alternate_url: HttpUrl
    snippet: Dict
    employer: Dict
    
    
class AbstractSaveFile(BaseModel, ABC):
    """Абстрактный класс для работы с файлами
    """    

    mode: str
    
    @abstractmethod
    def save_to_file(self, vacance, path):
        pass

    @abstractmethod
    def change_to_file(self, path):
        pass
    
    @abstractmethod
    def delete_of_file(self, path):
        pass