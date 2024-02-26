from pydantic import BaseModel, DirectoryPath
from abc import ABC, abstractmethod
from queue import Queue
from typing import Literal, Type
from csv import DictWriter

from queue import Queue

class AbstractSaveFile(BaseModel, ABC):

    mode: str
    
    @abstractmethod
    def save_to_file(self, vacance, path):
        pass

    @abstractmethod
    def change_to_file(self, path):
        pass
    
    @abstractmethod
    def delete_of_file(self, path):
        pass
        

class SaveToJson(AbstractSaveFile):
    
    mode: Literal['w', 'a'] = 'w'
  
    def save_to_file(self, vacance: Type[Queue], path: DirectoryPath ='vacancies.json'):
        with open(path, self.mode, encoding='utf-8') as file:
            while vacance.qsize() != 0:
                item = vacance.get()
                file.write(item.model_dump_json(indent=2))
                
    def change_to_file(self, path):
        pass
    
    def delete_of_file(self, path):
        pass
  
            
class SaveToText(AbstractSaveFile):
    
    mode: Literal['w', 'a'] = 'w'
       
    def save_to_file(self, vacance: Type[Queue], path: DirectoryPath ='vacancies.txt'):
        with open(path, self.mode, encoding='utf-8') as file:
            while vacance.qsize() != 0:
                item = vacance.get()
                file.write(item.model_dump_json().replace(('{'), '\n').replace('}', '\n'))
                
    def change_to_file(self, path):
        pass
    
    def delete_of_file(self, path):
        pass
    
class SaveToCsv(AbstractSaveFile):
    
    mode: Literal['w', 'a'] = 'w'
        
    def save_to_file(self, vacance: Type[Queue], path: DirectoryPath ='vacancies.csv'):
        with open(path, self.mode, encoding='utf-8') as file:
            file_csv = DictWriter(file, ('name', 'area', 'professional_roles', 'salary', 'alternate_url'))
            file_csv.writeheader()
            while vacance.qsize() != 0:
                item = vacance.get()
                file_csv.writerow(item.model_dump(exclude=('experience', 'schedule', 'snippet', 'employment', 'employer')))
                
    def change_to_file(self, path):
        pass
    
    def delete_of_file(self, path):
        pass
    
class SaveToDb(AbstractSaveFile):
    
    def save_to_file(self, vacance, path):
        pass
    
    def change_to_file(self, path):
        pass
    
    def delete_of_file(self, path):
        pass
