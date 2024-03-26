from typing import List, Dict, Union, Tuple
from src.hh_employes.employeer import VacanceTuple, CompaniesVacancies, AllVacancies, AVGSalary


class CorrectValues:
    """Класс корректирующий данные под нужный вид
    """    
    
    @classmethod
    def correct_list(cls, items: Dict) -> List:
        """Преобразует Словарь в Список(рекурсивно)
        """        
        
        correct_tuple = []
        
        for item in items.values():

            if type(item) != dict and type(item) != list:
                correct_tuple.append(item)
            elif type(item) == list:
                if len(item) != 0:
                    correct_tuple.extend(cls.correct_list(item[0]))
            else:
                correct_tuple.extend(cls.correct_list(item))
        
        return correct_tuple
    
    
    @classmethod
    def correct_name_companies(cls, list_companies: str) -> List[str]:
        """Преобразует строку из наименований компаний в список
        """ 
               
        result = list_companies.split(',')
        result = [item.strip() for item in result]
        return result
    
    
    @classmethod
    def correct_named_tuple(cls, model_parse: Union[VacanceTuple,
                                                   CompaniesVacancies,
                                                   AllVacancies,
                                                   AVGSalary],
                            list_tuple: List[Tuple]) -> Union[List[VacanceTuple],
                                                              List[CompaniesVacancies],
                                                              List[AllVacancies],
                                                              List[AVGSalary]]:
        """Преобразует список из кортежей в список из определенной модели

        Args:
            mode_parse (Union[VacanceTuple, CompaniesVacancies, AllVacancies, AVGSalary]): модель для парсинга кортежа
            list_tuple (List[Tuple]): список из кортежей

        Returns:
            Union[List[VacanceTuple], List[CompaniesVacancies], List[AllVacancies], List[AVGSalary]]: возращает список определенных моделей
        """                                
        
        result = [model_parse(*item) for item in list_tuple]
        return result
    