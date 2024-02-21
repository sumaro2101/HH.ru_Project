import pytest
from src.api_hh import HhVacancies

@pytest.fixture(scope='class')
def init_api():
    api_hh = HhVacancies(name='python', per_page=3, page=0)
    return api_hh