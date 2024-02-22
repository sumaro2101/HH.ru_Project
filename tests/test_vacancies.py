import pytest
from src.vacancies import Vacancy

@pytest.mark.vacancy
class TestVacancy:
    
    def test_vacancy(self, init_api):
        vacancy = Vacancy.model_validate(init_api.response[0])
        assert vacancy.name is not None