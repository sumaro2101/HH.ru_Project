import pytest
from src.hh_vacancies.vacancies import Vacancy

@pytest.mark.vacancy
class TestVacancy:
    
    def test_vacancy(self, test_model):
        vacancy = Vacancy.model_validate(test_model)
        
        assert vacancy.area.model_dump() == {'name': 'Москва'}