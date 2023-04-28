import psycopg2
# import data.queries


class DBManager:
    """"Класс обработки запросов к созданной БД PostgreSQL"""

    def __init__(self):
        self.base = 'base'  # Название используемой БД
        self.conn = psycopg2.connect(dbname=f'{self.base}', host='localhost', user='postgres', password='171717')
        pass

    def get_companies_and_vacancies_count(self):
        """получает список всех компаний и количество вакансий у каждой компании"""

        try:
            with self.conn.cursor() as cur:
                # формируем запрос
                cur.execute(f"select DISTINCT Employer.employer_name, count(Vacancy.name) as vacancy "
                            "from employer Join vacancy USING (id_employer)"
                            "GROUP BY Employer.employer_name")
                reqest = cur.fetchall()


        except:
            raise
        finally:
            self.conn.close()

        return reqest
    def get_all_vacancies(self):
        """получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию"""
        pass

    def get_avg_salary(self):
        """получает среднюю зарплату по вакансиям"""
        pass

    def get_vacancies_with_higher_salary(self):
        """получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        pass

    def get_vacancies_with_keyword(self):
        """получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”"""
        pass