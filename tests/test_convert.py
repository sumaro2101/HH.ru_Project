import pytest

@pytest.mark.convert
class TestConvert:
    
    def test_convert(self, init_api_convert, json_file):
        assert init_api_convert._make_list_for_convert(json_file) == ['USD', 'UZS']
        
    @pytest.mark.skip(reason='Закончились запросы в API Exchange')
    def test_rates(self, init_api_convert, json_file):
        print(init_api_convert.get_rate_currency(init_api_convert._make_list_for_convert(json_file)))
        assert init_api_convert.get_rate_currency(init_api_convert._make_list_for_convert(json_file)) is not None
         