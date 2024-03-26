from pydantic import Field, HttpUrl
from typing import NamedTuple
from decimal import Decimal

from src.abstract.abstract_classes import AbstractEmployeer


class Employeers(AbstractEmployeer):
    """Модель для парсинга и сеарилизации работадатель
    """    
    
    id_company: int = Field(alias='id')
    company_name: str = Field(alias='name')
    url_api: str = Field(alias='url')
    url_site: str = Field(alias='alternate_url')
    vacancies_url: str
    open_vacancies: int
    
    
class VacanceTuple(NamedTuple):
    """Модель для парсинга и сеарилизации вакансия 
    """
    
    id_vacancy: int
    name_vacancy: str
    area: str
    professional_roles: str
    salary_from: Decimal
    salary_to: Decimal
    salary_currency: str
    experience: str
    employment: str
    schedule: str
    alternate_url: HttpUrl
    employer_name: str
    employer_alternate_url: HttpUrl
    id_company: int
    
    
class CompaniesVacancies(NamedTuple):
    """Модель для парсинга и сеарилизации количества вакансий у работадателя
    """
    
    employer_name: str
    count_vacancies: int
    
    
class AllVacancies(NamedTuple):
    """Модель для парсинга и сеарилизации вакансий(краткая)
    """
    
    employer_name: str
    name_vacancy: str
    salary_from: Decimal
    salary_to: Decimal
    salary_currency: str
    alternate_url: HttpUrl
    
    
class AVGSalary(NamedTuple):
    """Модель для парсинга и сеарилизации средней зарплаты
    """
    
    average_saraly: Decimal
    