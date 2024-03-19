from queue import Queue
from typing import Type, Literal, Union

from src.hh_vacancies.api_hh import HhVacancies
from src.hh_vacancies.vacancies import Vacancy
from src.utils.save_file import SaveToJson, SaveToCsv, SaveToText


class StopUserProgram(Exception):
    ''' Остановка пользовательской программы '''
    
class EmptyResult(Exception):
    ''' Ошибка пустого ответа '''
    
    
class UserInteraction:
    """Класс-контроллер для взаимодействия с пользователем
    """    
    
    @classmethod
    def validate_int(cls, int_: str) -> bool:
        """Валидация строки которая является числом
        """    
            
        if not int_.isdigit() or int(int_) < 0:
            print('Введите число, число должно быть не меньше нуля')
            return False
        
        return True
    
    @classmethod
    def user_notification_choise(cls):
        print('Если нет, нажми Enter')
        print('Если да, введи любой символ')
        
    @classmethod
    def _ask_format(self, format: str, 
                    mode: Literal['w', 'a'], 
                    queue: Type[Queue]) -> None:
        """Метод-шаблон который в зависимости от полученного числа делает действие

        Args:
            format (str): Формат сохранения 
            mode (str): Тип записи
            queue (Type[Queue]): Очередь с объектами
        """ 
               
        match format:
            case '1':
                SaveToJson(mode=mode).save_to_file(vacance=queue)

            case '2':
                SaveToText(mode=mode).save_to_file(vacance=queue)

            case '3':
                SaveToCsv(mode=mode).save_to_file(vacance=queue)
  
    @classmethod         
    def _ask_mode(self, mode: Literal['1', '2']) -> Literal['w', 'a']:
        """Выбор типа записи
        """  
              
        match mode:
            case '1':
                return "w"
            case '2':
                return 'a'
                
    @classmethod
    def save_to_file(cls,
                     name: Union[str, None],
                     page: Union[int, None],
                     per_page: Union[int, None],
                     convert_to_RUB: bool, 
                     town: Union[str, None]):
        """Метод-ядро работы программы

        Args:
            name (Union[str, None]): Професcия
            page (Union[int, None]): Страница
            per_page (Union[int, None]): Количество объектов
            convert_to_RUB (bool): Конвертирование валюты
            town (Union[str, None]): Выбор города
        """  
              
        per_page = int(per_page)
        user_page = int(page)
        
        while True:
            if per_page == 0:
                print('К сожалению список вакансий пуст')
                break
            try:
                vacancies = HhVacancies(name=name, per_page=per_page, page=page, convert_to_RUB=convert_to_RUB, town=town)
                
                if len(vacancies.response) == 0:
                    raise EmptyResult
                
                print('Обработка информации успешно завершена!')
                
            except EmptyResult:
                per_page -= 1
                continue
            
            print(f'На странице {user_page}')
            print(f'Мы нашли {len(vacancies.response)} вакансий')
            print('Ты можешь отменить операцию')
            
            while True:
                print('\nВ какой тип файла ты хочешь сохранить результат?')
                print('1. JSON')
                print('2. TXT')
                print('3. CSV')
                print('Нечего из этого отменяет операцию')
                choice_format = input()
                if not choice_format or not choice_format.isdigit():
                    break
                
                if 0 < int(choice_format) < 4:
                    while True:
                        print('\n1. Хочешь переписать файл?')
                        print('2. Хочешь дополнить файл?')
                        choice_mode = input()
                        if not choice_mode.isdigit():
                            continue
                        if cls.validate_int(choice_mode) and int(choice_mode) < 3:
                            choice_mode = cls._ask_mode(mode=choice_mode)   
                        else:
                            continue
                        
                        queue_models = Queue()
                        [queue_models.put(Vacancy.model_validate(item)) for item in vacancies.response]
                        cls._ask_format(format=choice_format, mode=choice_mode, queue=queue_models)                  
                        break
                    
                    print('\nХочешь записать в другом формате?')
                    cls.user_notification_choise()
                    
                    if not input(): 
                        break
                    
                    continue

                else:
                    return
            break
        