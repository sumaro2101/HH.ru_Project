import pytest
import json
from src.hh_vacancies.api_hh import HhVacancies
from src.hh_vacancies.vacancies import Vacancy
from queue import Queue


@pytest.fixture(scope='class')
def json_file():
    with open('tests/test.json') as file:
        result = json.load(file)
        return result
            
@pytest.fixture(scope='class')
def init_api(json_file):
    api_hh = HhVacancies(name=None, per_page=None, page=None, town=None)
    api_hh._sort_json_response(HhVacancies ,json_file)
    return api_hh

@pytest.fixture(scope='class')
def init_api_convert(json_file):
    api_hh = HhVacancies(name=None, per_page=None, page=None, convert_to_RUB=True, town=None)
    api_hh._convert_valute(HhVacancies ,json_file)
    return api_hh

@pytest.fixture(scope='function')
def queue_full(init_api):
    vacancy = Queue()
    [vacancy.put(Vacancy.model_validate(item)) for item in init_api.response]
    return vacancy

@pytest.fixture(scope='function')
def temp_file(tmpdir_factory):
    file = tmpdir_factory.mktemp('data')
    return file

@pytest.fixture(scope='function')
def test_model():
    test_dict = {
        'id': 7289180,
        'name': 'Junior-разработчик',
        'area': {'id': '1', 'name': 'Москва', 'url': 'https://api.hh.ru/areas/1'},
        'professional_roles': [{'id': '96', 'name': 'Программист, разработчик'}],
        'salary': {'currency': 'EUR', 'from': 600, 'gross': False, 'to': 1200},
        'experience': {'id': 'noExperience', 'name': 'Нет опыта'},
        'employment': {'id': 'full', 'name': 'Полная занятость'},
        'schedule': {'id': 'fullDay', 'name': 'Полный день'},
        'alternate_url': 'https://hh.ru/vacancy/92961739',
        'snippet': {'requirement': 'Ты знаешь инструменты для обработки и анализа '
                             'данных, такие как Microsoft Excel, SQL, '
                             '<highlighttext>Python</highlighttext> или R; '
                             'умеешь работать с системами...',
              'responsibility': 'Demand Planning – анализ и прогнозирование '
                                'будущего спроса на товары и услуги. Supply '
                                'Chain Planning – стратегический подход к '
                                'управлению этапами создания...'},
        'employer': {'accredited_it_employer': False,
               'alternate_url': 'https://hh.ru/employer/9734048',
               'id': '9734048',
               'logo_urls': {'240': 'https://hhcdn.ru/employer-logo/6327175.png',
                             '90': 'https://hhcdn.ru/employer-logo/6327174.png',
                             'original': 'https://hhcdn.ru/employer-logo-original/1176687.png'},
               'name': 'Планетра',
               'trusted': True,
               'url': 'https://api.hh.ru/employers/9734048',
               'vacancies_url': 'https://api.hh.ru/vacancies?employer_id=9734048'}
    }
    return test_dict