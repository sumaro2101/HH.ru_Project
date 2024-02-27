from queue import Queue

from src.api_hh import HhVacancies
from src.vacancies import Vacancy
from src.save_file import SaveToJson, SaveToCsv, SaveToText


class StopUserProgram(Exception):
    ''' Остановка пользовательской программы '''
    
class EmptyResult(Exception):
    ''' Ошибка пустого ответа '''
    
    
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
                SaveToJson(mode=mode).save_to_file(vacance=queue)

            case '2':
                SaveToText(mode=mode).save_to_file(vacance=queue)

            case '3':
                SaveToCsv(mode=mode).save_to_file(vacance=queue)

            
    @classmethod         
    def _ask_mode(self, mode):
        match mode:
            case '1':
                return "w"
            case '2':
                return 'a'
                
    @classmethod
    def save_to_file(cls, name, page, per_page, convert_to_RUB, town):
        
        per_page = int(per_page)
        user_page = int(page)
        
        while True:
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