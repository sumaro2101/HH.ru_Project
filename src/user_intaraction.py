from queue import Queue
from pydantic import ValidationError

from src.api_hh import HhVacancies
from src.vacancies import Vacancy
from src.save_file import SaveToJson, SaveToCsv, SaveToText


class StopUserProgram(Exception):
    ''' Остановка пользовательской программы '''
    
    
class UserInteraction:
    
    @classmethod
    def validate_int(cls, int_):
        if not int_.isdigit() or int(int_) < 0:
            print('Введите цисло, цисло должно быть не меньше нуля')
            return False
        return True
    
    @classmethod
    def user_notification_choise(cls):
        print('Если нет, нажми Enter')
        print('Если да, введи любой символ')
        
    @classmethod
    def _ask_format(self, format, mode, queue):
        match format:
            case '1':
                SaveToJson(mode=mode).save_to_file(queue)
            case '2':
                SaveToText(mode=mode).save_to_file(queue)
            case '3':
                SaveToCsv(mode=mode).save_to_file(queue)
            
    @classmethod         
    def _ask_mode(self, mode):
        match mode:
            case '1':
                return "w"
            case '2':
                return 'a'
                
    @classmethod
    def save_to_file(cls, name, page, per_page, convert_to_RUB, town):
        
        vacancies = HhVacancies(name=name, per_page=per_page, page=page, convert_to_RUB=convert_to_RUB, town=town)
        
        if len(vacancies.response) == 0:
            print('К сожалению список вакансий пуст, попробуй выбрать другую страницу')
            print('Либо уменьшить количество вакансий')
            raise StopUserProgram
        
        queue_models = Queue()
        [queue_models.put(Vacancy.model_validate(item)) for item in vacancies.response]
        print('Обработка информации успешно завершена!')
        
        while True:
            print('\nВ какой тип файла ты хочешь сохранить результат?')
            print('1. JSON')
            print('2. TXT')
            print('3. CSV')
            print('Нечего из этого отменяет операцию')
            choice_format = input()
            if not choice_format:
                break
            
            if 0 < int(choice_format) < 4:
                while True:
                    print('\n1. Хочешь переписать файл?')
                    print('2. Хочешь дополнить файл?')
                    choice_mode = input()
                    
                    if cls.validate_int(choice_mode):
                        choice_mode = cls._ask_mode(mode=choice_mode)
                        
                    else:
                        continue
                    
                    cls._ask_format(format=choice_format, mode=choice_mode, queue=queue_models)                  
                    break
                
                print('\nХочешь записать в другом формате?')
                cls.user_notification_choise()
                if not input(): 
                    break
                continue

            else:
                return
            