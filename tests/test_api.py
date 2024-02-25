import pytest
from pydantic import ValidationError
from src.api_hh import HhVacancies

@pytest.mark.api
class TestApi:
    """Тест API HH
    """    
    
    def test_params(self, init_api):
        """Тест инициализированных параметров

        Args:
            init_api (fixture): инициализированная модель
        """    
            
        assert init_api.model_dump() == {'convert_to_RUB': False, 'name': 'python', 'page': 0, 'per_page': 3, 'town': None}
         
         
    def test_raise_name(self, init_api):
        """Тест исключения в случае попытки изменить параметр

        Args:
            init_api (fixture): инициализированная модель
        """  
              
        with pytest.raises(ValidationError):
            init_api.name = 'raise'
    
    
    def test_raise_page(self, init_api):
        """Тест исключения в случае попытки изменить параметр

        Args:
            init_api (fixture): инициализированная модель
        """  
        
        with pytest.raises(ValidationError):
            init_api.page = 'raise'
            
            
    def test_raise_per_page(self, init_api):
        """Тест исключения в случае попытки изменить параметр

        Args:
            init_api (fixture): инициализированная модель
        """  
        
        with pytest.raises(ValidationError):
            init_api.per_page = 'raise'
       
        
    def test_response_param(self, init_api):
        """Тест исключения в случае попытки изменить параметр

        Args:
            init_api (fixture): инициализированная модель
        """
    
        with pytest.raises(ValidationError):
            init_api.responce = []
    
            
    def test_raise_name_init(self):
        """Тест исключения в случае попытки инициализировать не правильный параметр

        Args:
            init_api (fixture): инициализированная модель
        """  
        
        with pytest.raises(ValidationError):
            HhVacancies(name=10)
            
    @pytest.mark.skip(reason='Этот тест зависит от состояния страницы, есть возможность существования страницы - не зависит от меня')       
    def test_raise_page_not_found(self):
        """Тест исключения в случае попытки получить не существующую страницу

        Args:
            init_api (fixture): инициализированная модель
        """  
        
        with pytest.raises(TypeError):
            HhVacancies(name='python', page=21)      
    
    
    def test_response(self, init_api):
        """Тест получения запроса

        Args:
            init_api (fixture): инициализированная модель
        """    
            
        assert len(init_api.response) == 3       
        