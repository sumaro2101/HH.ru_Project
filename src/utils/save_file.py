from pydantic import DirectoryPath
from queue import Queue
from typing import Literal, Type
from csv import DictWriter

from src.abstract.abstract_classes import AbstractSaveFile
        

class SaveToJson(AbstractSaveFile):
    """Класс для работы с файлами типа JSON
    """    
    
    mode: Literal['w', 'a'] = 'w'
  
    def save_to_file(self, vacance: Type[Queue],
                     path: DirectoryPath ='vacancies.json') -> None:
        """Сохранeние файла типа JSON

        Args:
            vacance (Type[Queue]): Очередь которая имеет ссылки на вакансии
            path (DirectoryPath, optional): _description_. Defaults to 'vacancies.json'.
        """  
              
        with open(path, self.mode, encoding='utf-8') as file:
            
            while vacance.qsize() != 0:
                item = vacance.get()
                file.write(item.model_dump_json(indent=2, by_alias=True))
                
    def change_to_file(self, path):
        pass
    
    def delete_of_file(self, path):
        pass
  
            
class SaveToText(AbstractSaveFile):
    """Класс для работы с файлами типа TXT
    """    
    
    mode: Literal['w', 'a'] = 'w'
       
    def save_to_file(self, vacance: Type[Queue],
                     path: DirectoryPath ='vacancies.txt') -> None:
        """Сохранeние файла типа TXT

        Args:
            vacance (Type[Queue]): Очередь которая имеет ссылки на вакансии
            path (DirectoryPath, optional): _description_. Defaults to 'vacancies.json'.
        """  
        
        with open(path, self.mode, encoding='utf-8') as file:
            
            while vacance.qsize() != 0:
                item = vacance.get()
                file.write(item.model_dump_json(by_alias=True).replace(('{'), '\n').replace('}', '\n'))
                
    def change_to_file(self, path):
        pass
    
    def delete_of_file(self, path):
        pass
    
    
class SaveToCsv(AbstractSaveFile):
    """Класс для работы с файлами типа CSV
    """    
    
    mode: Literal['w', 'a'] = 'w'
        
    def save_to_file(self, vacance: Type[Queue],
                     path: DirectoryPath ='vacancies.csv'):
        """Сохранeние файла типа CSV

        Args:
            vacance (Type[Queue]): Очередь которая имеет ссылки на вакансии
            path (DirectoryPath, optional): _description_. Defaults to 'vacancies.json'.
        """  
        
        with open(path, self.mode, encoding='utf-8') as file:
            
            file_csv = DictWriter(file, ('name', 'area', 'professional_roles', 'salary', 'alternate_url'))
            file_csv.writeheader()
            
            while vacance.qsize() != 0:
                item = vacance.get()
                file_csv.writerow(item.model_dump(by_alias=True, exclude=('experience', 'schedule', 'snippet', 'employment', 'employer')))
                
    def change_to_file(self, path):
        pass
    
    def delete_of_file(self, path):
        pass
    
    
class SaveToDb(AbstractSaveFile):
    """Класс для работы с БазойДанных
    """    
    
    def save_to_file(self, vacance, path):
        pass
    
    def change_to_file(self, path):
        pass
    
    def delete_of_file(self, path):
        pass
