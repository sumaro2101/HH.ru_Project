import pytest

@pytest.mark.convert
class TestConvert:
    def test_convert(self, init_api_convert):
        assert init_api_convert._make_list_for_convert() == ['USD']
         