from queue import Queue
import psycopg2
from psycopg2.errors import Error
import httpx
import asyncio
from typing import Type, Literal, Union

from src.hh_vacancies.api_hh import HhVacancies
from src.hh_vacancies.vacancies import Vacancy
from src.hh_employes.api_employee_hh import HhEmpoloyee
from src.hh_employes.employeer import Employeers
from src.utils.save_file import SaveToJson, SaveToCsv, SaveToText
from src.database.DBSetup import DbSetup
from src.database.DBManager import DbManager
from src.utils.correct_tuple import CorrectValues

COMPANIES = ['kt.team', 'Bell Integrator', 'НИИ Вектор', 'Компэл', 'FINAMP', 'Лаборатория Наносемантика', 'Тензор', 'Соломон', 'the_covert', 'На_Полке']
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
    
    @classmethod
    async def get_vacancies(cls ,companies):
        
        print(f'Вы выбрали {companies}')
        print('Создаем базу данных...')
        DbSetup.create_db()
        print('Создаем таблицы...')
        
        try:
            
            with psycopg2.connect(**DbSetup.config) as conn:
                with conn.cursor() as curr:
                    DbSetup.create_table_companies(curr)
                    DbSetup.create_table_vacancies(curr)
        finally:
            conn.close()
            
        print('Получаем информацию о работодателе...')
        
        async with httpx.AsyncClient() as session:
            request_list = []
            
            for company in companies:
                request_list.append(HhEmpoloyee(name=company, per_page=100, page=0, session=session).response)
                
            requests = await asyncio.gather(*request_list) 
            
        print('Сохраняем в базу данных работодателей...')
        
        company_ids = []
        companies_name = []          
        
        try:
            with psycopg2.connect(**DbSetup.config) as conn:
                with conn.cursor() as curr:

                    for item in requests:
                        
                        for elem in item['items']: 
                            if elem['name'] in companies and elem['name'] not in companies_name:
                                companies_name.append(elem['name'])
                                employeer = Employeers.model_validate(elem)
                                company_ids.append(employeer.id_company)
                                company_to_db = list(employeer.model_dump().values())
                            
                        try:
                            DbSetup.fill_companies(curr=curr, items=company_to_db)
                            
                        except Error:
                            print(f'Компания {employeer.company_name} уже была сохранена')
                            
                    print('Сохранение успешно завершено')
        finally:
            conn.close()
        
        print('Получаем вакансии от работодателей...')
        vacancies_of_id = HhVacancies(name=None, per_page=100, page=0, employer_id=company_ids, town=None).response
        vacancies = [Vacancy.model_validate(item) for item in vacancies_of_id]
        vacancies_to_db = [CorrectValues.correct_list(vacancy.model_dump(exclude=('snippet'))) for vacancy in vacancies]
        
        print(f'Было полученно {len(vacancies)} вакансий')
        print('Сохраняем вакансии в базу данных...')
      
        try:
            
            with psycopg2.connect(**DbSetup.config) as conn:
                with conn.cursor() as curr:
                    for vacancy in vacancies_to_db:
            
                        try:  
                            DbSetup.fill_vacancies(curr=curr, items=vacancy)
                        except Error:
                            print(f'Вакансия {vacancy[0]} уже записана') 
        
                                
                    print('Cохранение успешно завершено')
        finally:
            conn.close()

