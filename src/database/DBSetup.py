from src.database.config import config
from pydantic import BaseModel
from typing import ClassVar, Dict
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.errors import Error

class DbSetup(BaseModel):
    
    config: ClassVar[Dict] = config()
    db_name: ClassVar[str] = 'hhru'
    companies_table: ClassVar[str] = 'companies'
    vacancies_table: ClassVar[str] = 'vacancies'
    
    
    @classmethod
    def _get_connect(cls, config):
        connect = psycopg2.connect(**config)
        return connect
    
    
    @classmethod
    def create_db(cls):
        connect = cls._get_connect(cls.config)
        connect.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        curr = connect.cursor()
        
        try:
            create_db_sql = f'CREATE DATABASE {cls.db_name}'
            curr.execute(create_db_sql)
            
        except (Exception, Error):
            print(f'База Данных {cls.db_name} уже создана')
            
        finally:
            curr.close()
            connect.close()
        
        cls.config.update({'database': cls.db_name})
    
    
    @classmethod
    def create_table_companies(cls, curr):
                
        table = f'CREATE TABLE {cls.companies_table}\
            (id_company    int PRIMARY KEY,\
            company_name   varchar( 20 ) NOT NULL,\
            url_api        varchar( 100 ) NOT NULL,\
            url_site       varchar( 100 ) NOT NULL,\
            vacancies_url  varchar( 100 ) NOT NULL,\
            open_vacancies smallint NOT NULL);'
        try:    
            curr.execute(table)
        except Error:
            print(f'{cls.companies_table} уже создана')


    @classmethod
    def create_table_vacancies(cls, curr):
        
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
            employer_alternate_url text NOT NULL);'
        try:
            curr.execute(table)
        except Error:
            print(f'{cls.vacancies_table} уже создана')  
     
        
    @classmethod
    def add_foreign_key(cls, curr):
        
        try:
            curr.execute(f'ALTER TABLE {cls.vacancies_table}\
                ADD COLUMN id_company int;')
            
            curr.execute(f'ALTER TABLE {cls.vacancies_table}\
                ADD CONSTRAINT fk_vacancies_id_company\
                FOREIGN KEY ( id_company ) REFERENCES {cls.companies_table}( id_company )')
        except Error:
            print('Зависимости уже опеределены')    
    
    
    @classmethod
    def fill_companies(cls, curr, items):
        
        curr.execute(f'INSERT INTO {cls.companies_table}\
            VALUES (%s,%s,%s,%s,%s,%s);', items)
        
        
    @classmethod  
    def fill_vacancies(cls, curr, items):
        
        curr.execute(f'INSERT INTO {cls.vacancies_table}\
            (id_vacancy, name_vacancy, area, professional_roles, salary_from, salary_to,\
            salary_currency, experience, employment, schedule, alternate_url, employer_name, employer_alternate_url)\
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);', items)
     
     
    @classmethod
    def fill_id_company(cls, curr):
           
        curr.execute(f'UPDATE {cls.vacancies_table}\
            SET id_company = ( SELECT id_company FROM {cls.companies_table}\
            WHERE {cls.companies_table}.company_name = {cls.vacancies_table}.employer_name);')
        
