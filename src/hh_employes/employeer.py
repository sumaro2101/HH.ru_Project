from pydantic import BaseModel, ConfigDict, Field, HttpUrl
from typing import Union, List

from src.abstract.abstract_classes import AbstractEmployeer

class Employeers(AbstractEmployeer):
    
    id_company: int = Field(alias='id')
    company_name: str = Field(alias='name')
    url_api: str = Field(alias='url')
    url_site: str = Field(alias='alternate_url')
    vacancies_url: str
    open_vacancies: int