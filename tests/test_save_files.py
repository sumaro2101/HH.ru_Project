import pytest
from src.save_file import SaveToJson, SaveToText, SaveToCsv
import os
from pydantic import ValidationError

@pytest.mark.save
class TestSave:
    """Тесты связанные с сохранением файла
    """    
    
    def test_save_json(self, queue_full, temp_file):
        """Тест сохранения файла в формате JSON

        Args:
            queue_full (fixture): Заполненая очередь экземплярами модели
            temp_file (fixture): Временный путь в папке
        """     
           
        file = temp_file.join('vacancies.json')
        SaveToJson(mode='w').save_to_file(queue_full, path=file)
        
        assert os.stat(file).st_size != 0
        
        
    def test_save_text(self, queue_full, temp_file):
        """Тест сохранения файла в формате txt

        Args:
            queue_full (fixture): Заполненая очередь экземплярами модели
            temp_file (fixture): Временный путь в папке
        """
        
        file = temp_file.join('vacancies.txt')
        SaveToText(mode='w').save_to_file(queue_full, path=file)
        
        assert os.stat(file).st_size != 0
        
        
    def test_save_csv(self, queue_full, temp_file):
        """Тест сохранения файла в формате csv

        Args:
            queue_full (fixture): Заполненая очередь экземплярами модели
            temp_file (fixture): Временный путь в папке
        """
        
        file = temp_file.join('vacancies.csv')
        SaveToCsv(mode='w').save_to_file(queue_full, path=file)
        
        assert os.stat(file).st_size != 0
        
        
    def test_raise_save_json(self):
        """Тест исключения в случае указания не правильного режима
        """  
              
        with pytest.raises(ValidationError):
            SaveToJson(mode='b')
          
            
    def test_raise_save_text(self):
        """Тест исключения в случае указания не правильного режима
        """
        
        with pytest.raises(ValidationError):
            SaveToText(mode='b')
           
            
    def test_raise_save_csv(self):
        """Тест исключения в случае указания не правильного режима
        """
        
        with pytest.raises(ValidationError):
            SaveToCsv(mode='b')
