from src.abstract.abstract_classes import AbstractDb

class DbManager(AbstractDb):
    
    @classmethod
    def get_companies_and_vacancies_count(cls, curr):
        get_companies = 'SELECT employer_name, count(employer_name) as count_vacancies\
                            FROM vacancies\
                            GROUP BY employer_name;'
            
        curr.execute(get_companies)
        return curr.fetchall()
    
    @classmethod
    def get_all_vacancies(cls, curr):
        get_vacancies = 'SELECT employer_name, name_vacancy,\
                            salary_from, salary_to, salary_currency, alternate_url\
                            FROM vacancies;'
                        
        curr.execute(get_vacancies)
        return curr.fetchall()
    
    @classmethod
    def get_avg_salary(cls, curr):
        get_avg = 'SELECT AVG((salary_from + salary_to) / 2)::numeric(10,2)\
                    FROM vacancies;'

        curr.execute(get_avg)
        return curr.fetchall()
    
    @classmethod
    def get_vacancies_with_higher_salary(cls, curr):
        get_higher = 'SELECT * FROM vacancies\
                        WHERE ((salary_from + salary_to) / 2)::numeric(10,2) > \
                            (SELECT AVG((salary_from + salary_to) / 2)::numeric(10,2)\
                                FROM vacancies);'
                                
        curr.execute(get_higher)
        return curr.fetchall()
        
    @classmethod
    def get_vacancies_with_keyword(cls, curr, text):
        get_with_keyword = f"SELECT * FROM vacancies\
                                WHERE LOWER(name_vacancy) LIKE LOWER('%s%')"
                                
        curr.execute(get_with_keyword, text)
        return curr.fetchall()