from queue import Queue
import psycopg2
from psycopg2.errors import Error
from psycopg2.extensions import cursor
import httpx
from httpx import AsyncClient
import asyncio
from sys import exit
from typing import Type, Literal, Union, List, Callable, Coroutine, Any

from src.hh_vacancies.api_hh import HhVacancies
from src.hh_vacancies.vacancies import Vacancy
from src.hh_employes.api_employee_hh import HhEmpoloyee
from src.hh_employes.employeer import Employeers
from src.utils.save_file import SaveToJson, SaveToCsv, SaveToText
from src.database.DBSetup import DbSetup
from src.database.DBManager import DbManager
from src.utils.correct_values import CorrectValues
from src.hh_employes.employeer import VacanceTuple, CompaniesVacancies, AllVacancies, AVGSalary

#Стандартный список компаний
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
    def _truncate_tables(cls, curr: cursor, checker: bool) -> None:
        """Очищает таблицы если они заполнены

        Args:
            checker (bool): метод проверяющий заполненость таблиц
        """        
        
        if checker:
            print('\nВ базе данных есть записи, хочешь перезаписать их?\n')
            cls.user_notification_choise()
            if input():
                DbManager.delete_data_tables(curr)
                print('База данных была очищена')
        
            
    @classmethod
    async def _get_list_companies(cls, companies: List[str], session: AsyncClient) -> Callable[..., Coroutine]:
        """Асинхронный метод запросов работадателей
        """        
        
        request_list = []
            
        for company in companies:
                request_list.append(HhEmpoloyee(name=company, per_page=100, page=0, session=session).response)                
            
        return await asyncio.gather(*request_list) 
    
    
    @classmethod
    def _get_town(cls, curr: cursor) -> None:
        """Поиск вакансий по городу
        """        
        
        print('Какой город ты ищещь?')
        
        list_of_town = [item[0] for item in DbManager.get_count_town(curr=curr)]
        
        while True:
            print('У тебя есть выбор из таких городов:')
            print(', '.join(list_of_town))
            print('Если хочешь остановить поиск нажми enter')
            choise = input()
            if choise:
                if choise in list_of_town:
                    print(f'Поиск по городу {choise}...')
                    result = DbManager.get_vacancies_of_town(curr=curr, town=choise)
                    print(f'Мы нашли {len(result)} вакансий в вашом городе')
                    return result
                
                else:
                    print('Такого города нет')
                    continue
            else:
                break
    
    
    @classmethod
    def _get_keyword(cls, curr: cursor) -> None:
        """Поиск вакансий по имени
        """        
        
        while True:
            print('\nКакое слово ты хочешь назвать?')
            print('Если хочешь отменить поиск нажми enter')
            key_word = input()
            
            if key_word:
                choice_format_data = DbManager.get_vacancies_with_keyword(curr=curr, text=key_word)
                
                if choice_format_data:
                    print(f'Поиск по слову {key_word} дал результат в виде {len(choice_format_data)} вакансий\n')
                    return choice_format_data
                else:
                    print('Поиск не дал результатов')
                    print('Хочешь продолжить?\n')
                    cls.user_notification_choise()
                    
                    if input():
                        continue
                    else:
                        break
            else:
                break
    
    
    @classmethod
    def _save_list_companies_into_db(cls, curr: cursor, list_companies: List, companies_name_check: List[str]) -> List[int]:
        """Сохранение компаний в таблицу

        Args:
            curr (cursor): курсор подключения
            list_companies (List): список компаний для сохранения
            companies_name_check (List[str]): список компаний для проверки дублироемости

        Returns:
            List[int]: возвращает список с айди сохраненых компаний для дальнейшей обработки
        """        
        
        company_ids = []
        companies_name = [] 
        count_iteraction = -1    
        
        for item in list_companies:
            count_iteraction += 1
            company_to_db = None 
                       
            for elem in item['items']: 
                if elem['name'] in companies_name_check and elem['name'] not in companies_name:
                    employeer = Employeers.model_validate(elem)
                    
                    company_ids.append(employeer.id_company)
                    companies_name.append(elem['name'])
                    company_to_db = list(employeer.model_dump().values())
                
            try:
                if company_to_db:
                    DbSetup.fill_companies(curr=curr, items=company_to_db)
                else:
                    raise ValueError
            except ValueError:
                print(f'Компания {companies_name_check[count_iteraction]} не существует')  
            except Error:
                print(f'Компания {employeer.company_name} уже была сохранена')
            
        print('Сохранение успешно завершено')
        
        return company_ids
    
    
    @classmethod
    def _requst_to_save(cls, item_to_save: Any) -> None:
        """Метод для сохранения данных в файлы
        """        
        
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
                    
                    if type(item_to_save) == HhVacancies:
                        queue_models = Queue()
                        [queue_models.put(Vacancy.model_validate(item)) for item in item_to_save.response]
                        cls._ask_format(format=choice_format, mode=choice_mode, queue=queue_models)                  
                        break
                    else:
                        cls._ask_format(format=choice_format, mode=choice_mode, queue=item_to_save) 
                        break
                    
                print('\nХочешь записать в другом формате?')
                cls.user_notification_choise()
                print('Если хочешь закрыть программу нажми "1"')
                choice = input()
                
                if choice == '1':
                    print('\nДо встречи странник! Да прибудет с тобой Таллос!')
                    exit()
                    
                if not choice: 
                    break
                
                continue

            else:
                return
            
            
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
            cls._requst_to_save(item_to_save=vacancies)
            
            break
    
    
    @classmethod
    async def get_vacancies(cls, companies: List[str]) -> None:
        """Ядро программы для обработки компаний и вакансий

        Args:
            companies (List[str]): Список компаний для обработки
        """ 
        #Основной цикл для работы всей программы      
        while True:
            #Создание базы данных
            print(f'\nВы выбрали {companies}')
            print('Создаем базу данных...')
            DbSetup.create_db()
            print('\nСоздаем таблицы...')
            
            try:
                #Создание таблиц
                with psycopg2.connect(**DbSetup.config) as conn:
                    with conn.cursor() as curr:
                        DbSetup.create_table_companies(curr)
                        DbSetup.create_table_vacancies(curr)
            finally:
                conn.close()
                
            try:
                #Очистка старых данных по требованию
                with psycopg2.connect(**DbSetup.config) as conn:
                    with conn.cursor() as curr:
                       cls._truncate_tables(curr=curr, checker=DbManager.check_fill_table(curr)[0][0])
            finally:
                conn.close()
                
            print('\nПолучаем информацию о работодателей...')
            #Асинхронные запросы на получениие данных всех работадателей из списка
            async with httpx.AsyncClient() as session:
                list_companies = await cls._get_list_companies(companies=companies, session=session)
                    
            print('\nСохраняем в базу данных работадателей...')
            
            try:
                #Сохранение работадателей в таблицу
                with psycopg2.connect(**DbSetup.config) as conn:
                    with conn.cursor() as curr:
                        company_ids = cls._save_list_companies_into_db(curr=curr, list_companies=list_companies, companies_name_check=companies)      
            finally:
                conn.close()
            
            print('\nПолучаем вакансии от работадателей...')
            
            page = 0
            #Цикл поиска вакансий от работадателей
            while True:
                
                #Поиск вакансий от работадателей
                if not company_ids:
                    print('Нет работадалетей для поиска\n')
                    break
                vacancies_of_id = HhVacancies(name=None, per_page=100, page=page, employer_id=company_ids, town=None, convert_to_RUB=True).response
                vacancies = [Vacancy.model_validate(item) for item in vacancies_of_id]
                vacancies_to_db = [CorrectValues.correct_list(vacancy.model_dump(exclude=('snippet'))) for vacancy in vacancies]
                
                print(f'\nБыло полученно {len(vacancies)} вакансий')
                print('Сохраняем вакансии в базу данных...')
            
                try:
                    #Сохранение вакансий в таблицу
                    with psycopg2.connect(**DbSetup.config) as conn:
                        with conn.cursor() as curr:
                            for vacancy in vacancies_to_db:
                                try:  
                                    DbSetup.fill_vacancies(curr=curr, items=vacancy)
                                except Error:
                                    print(f'Вакансия {vacancy[0]} уже записана') 
                            print('Cохранение успешно завершено\n')
                finally:
                    conn.close()
                    
                    if len(vacancies) == 0:
                        print('К сожалению вакансий больше нет\n')
                        break
                    if len(vacancies) == 100:
                        print('\nНужно больше вакансий?')
                        cls.user_notification_choise()
                        if input():
                            page += 1
                            continue
                        else:
                            break
                    break
            #Цикл для вывода данных и сохранения в файлы   
            while True:
                #Список возможных вариантов вывода данных
                if not company_ids:
                    break
                print('\nВыбери в каком виде ты хочешь получить данные')
                print('1.Cписок всех компаний и количество вакансий у каждой компании')
                print('2.Cписок всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию')
                print('3.Средняя зарпалата по вакансиям')
                print('4.Cписок всех вакансий, у которых зарплата выше средней по всем вакансиям.')
                print('5.Cписок всех вакансий, в названии которых содержатся переданные в метод слова, например python.')
                print('6.Список всех вакансий по определенном городу\n')
                choice_format_data = input()
                if not choice_format_data:
                    break
                try:
                    #Вывод данных исходя из выбора в списке
                    with psycopg2.connect(**DbSetup.config) as conn:
                        with conn.cursor() as curr:
                            match choice_format_data:
                                case '1':
                                    choice_format_data = DbManager.get_companies_and_vacancies_count(curr=curr)
                                    list_of_vacancies_save = CorrectValues.correct_named_tuple(model_parse=CompaniesVacancies, list_tuple=choice_format_data)
                                case '2':
                                    choice_format_data = DbManager.get_all_vacancies(curr=curr)
                                    list_of_vacancies_save = CorrectValues.correct_named_tuple(model_parse=AllVacancies, list_tuple=choice_format_data)
                                case '3':
                                    choice_format_data = DbManager.get_avg_salary(curr=curr)
                                    list_of_vacancies_save = CorrectValues.correct_named_tuple(model_parse=AVGSalary, list_tuple=choice_format_data)
                                case '4':
                                    choice_format_data = DbManager.get_vacancies_with_higher_salary(curr=curr)
                                    list_of_vacancies_save = CorrectValues.correct_named_tuple(model_parse=VacanceTuple, list_tuple=choice_format_data)
                                case '5':
                                    choice_format_data = cls._get_keyword(curr=curr)
                                    if choice_format_data:
                                        list_of_vacancies_save = CorrectValues.correct_named_tuple(model_parse=VacanceTuple, list_tuple=choice_format_data)
                                case '6':
                                    choice_format_data = cls._get_town(curr=curr)
                                    if choice_format_data:
                                        list_of_vacancies_save = CorrectValues.correct_named_tuple(model_parse=VacanceTuple, list_tuple=choice_format_data)
                                case _:
                                    print('Введены не корректные данные\n')
                                    continue
                finally:
                    conn.close()
                #Метод сохранения данных в файлы(В методе цикл)   
                if choice_format_data:
                    cls._requst_to_save(item_to_save=list_of_vacancies_save)
                else:
                    print('Хочешь выбрать другие варианты выборки?')
                    cls.user_notification_choise()
                    if input():
                        continue
                   
            print('\nХочешь повторить поиск по работадателям?')
            cls.user_notification_choise()
            
            if input():
                print('\nНапиши через запятую(",") интересующие тебя компании')
                print(f'Если пропустишь то выберется стандартный набор компаний {COMPANIES}\n')
                companies = input()
                
                if companies:
                    companies = CorrectValues.correct_name_companies(companies)
                    continue
                else:
                    companies = COMPANIES
                    continue  
            break
        