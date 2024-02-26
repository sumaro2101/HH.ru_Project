import pytest

@pytest.mark.fixture
class TestFixture:
    
        
    def test_response(self, init_api):
        print(init_api.response)
        assert len(init_api.response) == 5
        
    def test_full_queue(self, queue_full):
        assert queue_full.qsize() == 5
    