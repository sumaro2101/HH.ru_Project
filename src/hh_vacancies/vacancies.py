from pydantic import BaseModel, ConfigDict, Field, HttpUrl
from typing import Union, List

from src.abstract.abstract_classes import AbstractVacancies
    
class Area(BaseModel):
    name: Union[str, None]
    
class ProfessionalRoles(BaseModel):
    name: Union[str, None]

class Salary(BaseModel):
    from_: Union[int, None] = Field(alias='from')
    to: Union[int, None]
    currency: str

class Experience(BaseModel):
    name: Union[str, None]
    
class Employment(BaseModel):
    name: Union[str, None]
    
class Schedule(BaseModel):
    name: Union[str, None]
    
class Snippet(BaseModel):
    requirement: Union[str, None]
    responsibility: Union[str, None]
    
class Employer(BaseModel):
    name : Union[str, None]
    alternate_url: Union[str, None]
    id_: int = Field(alias='id')
   
    
class Vacancy(AbstractVacancies):
    """Модель для сериализации данных а так же обработки
    """    
    
    model_config = ConfigDict(frozen=True)
    
    id_: int = Field(alias='id')
    name: str
    area: Area 
    professional_roles: List[ProfessionalRoles]
    salary: Salary
    experience: Experience
    employment: Employment
    schedule: Schedule
    alternate_url: str
    snippet: Snippet
    employer: Employer
