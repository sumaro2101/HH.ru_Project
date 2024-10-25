import json
from pydantic import DirectoryPath
from queue import Queue
from typing import Literal, Type, Union, List
from csv import DictWriter

from src.abstract.abstract_classes import AbstractSaveFile
from src.hh_employes.employeer import VacanceTuple, CompaniesVacancies, AllVacancies, AVGSalary
        

class SaveToJson(AbstractSaveFile):
    """Класс для работы с файлами типа JSON
    """    
    
    mode: Literal['w', 'a'] = 'w'
  
    def save_to_file(self, vacance: Union[Type[Queue],
                                          List[Type[VacanceTuple]],
                                               List[Type[CompaniesVacancies]],
                                               List[Type[AllVacancies]],
                                               List[Type[AVGSalary]],
                                          List[List]],
                     path: DirectoryPath ='vacancies.json') -> None:
        """Сохранeние файла типа JSON

        Args:
            vacance (Type[Queue]): Очередь которая имеет ссылки на вакансии
            path (DirectoryPath, optional): _description_. Defaults to 'vacancies.json'.
        """  
              
        with open(path, self.mode, encoding='utf-8') as file:
            
            if type(vacance) == Queue:
                while vacance.qsize() != 0:
                    item = vacance.get()
                    file.write(item.model_dump_json(indent=2, by_alias=True))
            elif type(vacance[0]) != list:
                file.write(json.dumps([item._asdict() for item in vacance], ensure_ascii=False, indent=2, default=str))
            else: 
                file.write(json.dumps(vacance, ensure_ascii=False, indent=1, default=str))
                
    def change_to_file(self, path):
        pass
    
    def delete_of_file(self, path):
        pass
  
            
class SaveToText(AbstractSaveFile):
    """Класс для работы с файлами типа TXT
    """    
    
    mode: Literal['w', 'a'] = 'w'
       
    def save_to_file(self, vacance: Union[Type[Queue],
                                          List[Type[VacanceTuple]],
                                               List[Type[CompaniesVacancies]],
                                               List[Type[AllVacancies]],
                                               List[Type[AVGSalary]],
                                          List[List]],
                     path: DirectoryPath ='vacancies.txt') -> None:
        """Сохранeние файла типа TXT

        Args:
            vacance (Type[Queue]): Очередь которая имеет ссылки на вакансии
            path (DirectoryPath, optional): _description_. Defaults to 'vacancies.json'.
        """  
        
        with open(path, self.mode, encoding='utf-8') as file:
            if type(vacance) == Queue:
                while vacance.qsize() != 0:
                    item = vacance.get()
                    file.write(item.model_dump_json(by_alias=True).replace(('{'), '\n').replace('}', '\n'))
            elif type(vacance[0]) != list:
                file.write(json.dumps([item._asdict() for item in vacance], ensure_ascii=False, indent=2, default=str).replace(('{'), '\n').replace('}', '\n'))
            else:
                file.write(json.dumps(vacance, ensure_ascii=False, default=str).replace((','), '\n').replace((']'), '\n').replace((','), '\n').replace(('['), '\n'))
                
    def change_to_file(self, path):
        pass
    
    def delete_of_file(self, path):
        pass
    
    
class SaveToCsv(AbstractSaveFile):
    """Класс для работы с файлами типа CSV
    """    
    
    mode: Literal['w', 'a'] = 'w'
        
    def save_to_file(self, vacance: Union[Type[Queue],
                                          List[Type[VacanceTuple]],
                                               List[Type[CompaniesVacancies]],
                                               List[Type[AllVacancies]],
                                               List[Type[AVGSalary]],
                                          List[List]],
                     path: DirectoryPath ='vacancies.csv'):
        """Сохранeние файла типа CSV

        Args:
            vacance (Type[Queue]): Очередь которая имеет ссылки на вакансии
            path (DirectoryPath, optional): _description_. Defaults to 'vacancies.json'.
        """  
        
        with open(path, self.mode, encoding='utf-8') as file:
            if type(vacance) == Queue:
                file_csv = DictWriter(file, ('name', 'area', 'professional_roles', 'salary', 'alternate_url'))
                file_csv.writeheader()
                
                while vacance.qsize() != 0:
                    item = vacance.get()
                    file_csv.writerow(item.model_dump(by_alias=True, exclude=('experience', 'schedule', 'snippet', 'employment', 'employer')))
            else:
                file_csv = DictWriter(file, vacance[0]._fields)
                file_csv.writeheader()
                [file_csv.writerow(item._asdict()) for item in vacance]
                  
    def change_to_file(self, path):
        pass
    
    def delete_of_file(self, path):
        pass
    