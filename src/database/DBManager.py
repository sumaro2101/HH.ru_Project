from src.abstract.abstract_classes import AbstractDb
from psycopg2.extensions import cursor
from typing import List, Tuple

class DbManager(AbstractDb):
    
    
    @classmethod
    def get_companies_and_vacancies_count(cls, curr: cursor) -> List[Tuple]:
        """Выводит количество вакансий в виде цифры в каждой из компаний
        """    
            
        get_companies = 'SELECT employer_name, count(employer_name) as count_vacancies\
                            FROM vacancies\
                            GROUP BY employer_name;'
            
        curr.execute(get_companies)
        return curr.fetchall()
    
    
    @classmethod
    def get_all_vacancies(cls, curr: cursor) -> List[Tuple]:
        """Выводит все вакансии
        """   
             
        get_vacancies = 'SELECT employer_name, name_vacancy,\
                            salary_from, salary_to, salary_currency, alternate_url\
                            FROM vacancies\
                            ORDER BY salary_from DESC;'
                        
        curr.execute(get_vacancies)
        return curr.fetchall()
    
    
    @classmethod
    def get_avg_salary(cls, curr: cursor) -> List[Tuple]:
        """Выводит среднюю зарплату по всем вакансиям
        """  
              
        get_avg = 'SELECT AVG((salary_from + salary_to) / 2)::numeric(10,2) as average_saraly\
                    FROM vacancies;'

        curr.execute(get_avg)
        return curr.fetchall()
    
    
    @classmethod
    def get_vacancies_with_higher_salary(cls, curr: cursor) -> List[Tuple]:
        """Выводит вакансии выше средней зарплаты по вакансиям
        """ 
               
        get_higher = 'SELECT * FROM vacancies\
                        WHERE ((salary_from + salary_to) / 2)::numeric(10,2) > \
                            (SELECT AVG((salary_from + salary_to) / 2)::numeric(10,2)\
                                FROM vacancies)\
                        ORDER BY ((salary_from + salary_to) / 2)::numeric(10,2) DESC;'
                                
        curr.execute(get_higher)
        return curr.fetchall()
        
        
    @classmethod
    def get_vacancies_with_keyword(cls, curr: cursor, text: str) -> List[Tuple]:
        """Выводит вакансии по имени
        """        
        get_with_keyword = f"SELECT * FROM vacancies\
                                WHERE LOWER(name_vacancy) LIKE LOWER('%{text}%')\
                                ORDER BY salary_from DESC; "
                                
        curr.execute(get_with_keyword)
        return curr.fetchall()
    
    
    @classmethod
    def get_vacancies_of_town(cls, curr: cursor, town: str) -> List[Tuple]:
        """Выводит вакансии по городу
        """        
        get_with_keyword = f"SELECT * FROM vacancies\
                                WHERE LOWER(area) LIKE LOWER('%{town}%')\
                                ORDER BY salary_from DESC; "
                                
        curr.execute(get_with_keyword)
        return curr.fetchall()
    
    
    @classmethod
    def get_count_vacancies(cls, curr: cursor) -> List[Tuple]:
        """Выводит общее количество вакансий
        """     
           
        get_count = 'SELECT count( * ) FROM vacancies;'
        
        curr.execute(get_count)
        return curr.fetchall()
    
    
    @classmethod
    def get_count_town(cls, curr: cursor) -> List[Tuple]:
        """Выводит все города которые присутствуют в вакансиях
        """ 
               
        get_count = 'SELECT area FROM vacancies\
                        GROUP BY (area)\
                            ORDER BY (area);'
    
        curr.execute(get_count)
        return curr.fetchall()
    
    
    @classmethod
    def delete_data_tables(cls, curr: cursor) -> List[Tuple]:
        """Удаляет всю информацию с таблиц
        """ 
               
        delete_data_vacancies = 'TRUNCATE TABLE vacancies CASCADE;'
        delete_data_companies = 'TRUNCATE TABLE companies CASCADE;'
        
        curr.execute(delete_data_vacancies)
        curr.execute(delete_data_companies)
        
        
    @classmethod
    def check_fill_table(cls, curr: cursor) -> List[Tuple]:
        """Возвращает True или False если таблица заполнена
        """
                
        check_table = 'SELECT EXISTS(SELECT * FROM vacancies);'
        
        curr.execute(check_table)
        return curr.fetchall()
    