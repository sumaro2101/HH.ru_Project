import pytest
from src.enum_town import EnumTown
from src.api_hh import HhVacancies

@pytest.mark.enum
class TestEnum:
    
    def test_enum(self):
        assert EnumTown.Астрахань.value == 15
        
    def test_id(self, init_api):
        assert init_api.make_id_of_town('Москва') == 1
