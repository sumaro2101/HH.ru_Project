from src.database.config import config
from pydantic import BaseModel
from typing import ClassVar, Dict, List, Union, Tuple

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT, connection, cursor
from psycopg2.errors import Error

class DbSetup(BaseModel):
    """Класс создания базы данных и создания таблиц
    """    
    
    config: ClassVar[Dict] = config()
    db_name: ClassVar[str] = 'hhru'
    companies_table: ClassVar[str] = 'companies'
    vacancies_table: ClassVar[str] = 'vacancies'
    
    
    @classmethod
    def _get_connect(cls, config: Dict) -> connection:
        """Подключение к среде psql
        """   
             
        connect = psycopg2.connect(**config)
        return connect
    
    
    @classmethod
    def create_db(cls) -> None:
        """Cоздание базы данных
        """    
            
        connect = cls._get_connect(cls.config)
        connect.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        curr = connect.cursor()
        
        try:
            create_db_sql = f'CREATE DATABASE {cls.db_name}'
            curr.execute(create_db_sql)
            print(f'База данных {cls.db_name} успешно создана\n')
            
        except (Exception, Error):
            print(f'База Данных {cls.db_name} уже создана\n')
            
        finally:
            curr.close()
            connect.close()
        
        cls.config.update({'database': cls.db_name})
    
    
    @classmethod
    def create_table_companies(cls, curr: cursor) -> None:
        """Создание таблицы компании
        """        
                
        table = f'CREATE TABLE {cls.companies_table}\
            (id_company    int PRIMARY KEY,\
            company_name   varchar( 50 ) NOT NULL,\
            url_api        varchar( 100 ) NOT NULL,\
            url_site       varchar( 100 ) NOT NULL,\
            vacancies_url  varchar( 100 ) NOT NULL,\
            open_vacancies smallint NOT NULL);'
        try:    
            curr.execute(table)
            print(f'Таблица {cls.companies_table} успешно создана')
        except Error:
            print(f'{cls.companies_table} уже создана')


    @classmethod
    def create_table_vacancies(cls, curr: cursor) -> None:
        """Создание таблицы вакансии
        """        
        
        table = f'CREATE TABLE {cls.vacancies_table}\
            (id_vacancy            int PRIMARY KEY,\
            name_vacancy           text NOT NULL,\
            area                   text NOT NULL,\
            professional_roles     text NOT NULL,\
            salary_from            numeric,\
            salary_to              numeric,\
            salary_currency        varchar( 3 ) NOT NULL CHECK ( salary_currency = UPPER( salary_currency )),\
            experience             text,\
            employment             text,\
            schedule               text,\
            alternate_url          text NOT NULL,\
            employer_name          text NOT NULL,\
            employer_alternate_url text NOT NULL,\
            id_company             int REFERENCES {cls.companies_table}(id_company));'
            
        try:
            curr.execute(table)
            print(f'Таблица {cls.vacancies_table} успешно создана\n')
        except Error:
            print(f'{cls.vacancies_table} уже создана\n')  
     
     
    @classmethod
    def fill_companies(cls, curr: cursor, items: Union[List, Tuple]) -> None:
        """Заполнение таблицы компании данными
        """
                
        curr.execute(f'INSERT INTO {cls.companies_table}\
            VALUES (%s,%s,%s,%s,%s,%s);', items)

        
    @classmethod  
    def fill_vacancies(cls, curr: cursor, items: Union[List, Tuple]) -> None:
        """Заполнение таблицы вакансии данными
        """
                
        curr.execute(f'INSERT INTO {cls.vacancies_table}\
            ( name_vacancy, area, professional_roles, salary_from, salary_to,\
            salary_currency, experience, employment, schedule, alternate_url,\
            employer_name, employer_alternate_url, id_company, id_vacancy )\
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);', items)
         