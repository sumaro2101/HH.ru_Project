from pydantic import BaseModel, ConfigDict, Field, HttpUrl
from abc import ABC
from typing import Union, Dict, List


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
    
class Area(BaseModel):
    name: Union[str, None]
    
class ProfessionalRoles(BaseModel):
    name: Union[str, None]

class Salary(BaseModel):
    from_: Union[int, None] = Field(alias='from')
    to: Union[int, None]
    
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
    alternate_url: Union[HttpUrl, None]
   
    
class Vacancy(AbstractVacancies):
    model_config = ConfigDict(frozen=True)
    
    name: str
    area: Area
    professional_roles: List[ProfessionalRoles]
    salary: Salary
    experience: Experience
    employment: Employment
    schedule: Schedule
    alternate_url: HttpUrl
    snippet: Snippet
    employer: Employer
    
    
b = {'accept_incomplete_resumes': False,
  'accept_temporary': True,
  'address': None,
  'adv_context': None,
  'adv_response_url': None,
  'alternate_url': 'https://hh.ru/vacancy/93633836',
  'apply_alternate_url': 'https://hh.ru/applicant/vacancy_response?vacancyId=93633836',
  'archived': False,
  'area': {'id': '2734',
           'name': 'Иннополис',
           'url': 'https://api.hh.ru/areas/2734'},
  'contacts': None,
  'created_at': '2024-02-21T22:38:09+0300',
  'department': None,
  'employer': {'accredited_it_employer': False,
               'alternate_url': 'https://hh.ru/employer/9176780',
               'id': '9176780',
               'logo_urls': None,
               'name': 'Ришат',
               'trusted': True,
               'url': 'https://api.hh.ru/employers/9176780',
               'vacancies_url': 'https://api.hh.ru/vacancies?employer_id=9176780'},
  'employment': {'id': 'full', 'name': 'Полная занятость'},
  'experience': {'id': 'between1And3', 'name': 'От 1 года до 3 лет'},
  'has_test': False,
  'id': '93633836',
  'insider_interview': None,
  'is_adv_vacancy': False,
  'name': 'Python Backend Developer (Django)',
  'premium': False,
  'professional_roles': [{'id': '96', 'name': 'Программист, разработчик'}],
  'published_at': '2024-02-21T22:38:09+0300',
  'relations': [],
  'response_letter_required': False,
  'response_url': None,
  'salary': {'currency': 'RUR', 'from': 50000, 'gross': False, 'to': None},
  'schedule': {'id': 'remote', 'name': 'Удаленная работа'},
  'snippet': {'requirement': 'Технологический стек: '
                             '<highlighttext>Python</highlighttext>, Django, '
                             'PostgreSQL, REST API, Docker, Git. Ответственный '
                             'и творческий подход к решению задач. '
                             'Приветствуется опыт трекинга задач...',
              'responsibility': 'Участие в разработке сервисов, согласно '
                                'техническому заданию. Реализация REST API, '
                                'обработка платежей, работа с email-рассылками '
                                'и другие классические задачи...'},
  'sort_point_distance': None,
  'type': {'id': 'open', 'name': 'Открытая'},
  'url': 'https://api.hh.ru/vacancies/93633836?host=hh.ru',
  'working_days': [],
  'working_time_intervals': [],
  'working_time_modes': []}
    
a = Vacancy.model_validate(b)
print(a.model_dump_json(indent=2))
