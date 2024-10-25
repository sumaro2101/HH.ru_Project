import pytest
from src.utils.enum_town import EnumTown

@pytest.mark.enum
class TestEnum:
    
    def test_enum(self):
        assert EnumTown.Астрахань.value == 15
        
    def test_id(self, init_api):
        assert init_api.make_id_of_town('Москва') == 1
