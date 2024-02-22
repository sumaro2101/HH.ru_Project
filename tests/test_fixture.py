import pytest

@pytest.mark.fixture
class TestFixture:
    
    def test_instanse_param(self, init_api):
        assert init_api.name == 'python'
        
    def test_response(self, init_api):
        assert len(init_api.response) == 3