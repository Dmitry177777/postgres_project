import psycopg2


class DBManager:
    """"Класс обработки запросов к созданной БД PostgreSQL"""

    def __init__(self):
        self.base = 'base'  # Название используемой БД

        pass

    def bd(self):
        return psycopg2.connect(dbname=f'{self.base}', host='localhost', user='postgres', password='171717')

    def get_companies_and_vacancies_count(self):
        """получает список всех компаний и количество вакансий у каждой компании"""
        conn = self.bd()
        try:
            with conn.cursor() as cur:
                # формируем запрос
                cur.execute(f"select DISTINCT Employer.employer_name, count(Vacancy.name) as vacancy "
                            "from employer Join vacancy USING (id_employer)"
                            "GROUP BY Employer.employer_name")
                reqest = cur.fetchall()


        except:
            raise
        finally:
            conn.close()

        return reqest
    def get_all_vacancies(self):
        """получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию"""
        conn = self.bd()
        try:
            with conn.cursor() as cur:
                # формируем запрос
                cur.execute(f"select Employer.employer_name, Vacancy.name,  Vacancy.salary_from, Vacancy.salary_to, Vacancy.salary_currency,Vacancy.response_url "
                            "from employer Join vacancy USING (id_employer)")
                reqest = cur.fetchall()

        except:
            raise
        finally:
            conn.close()

        return reqest

    def get_avg_salary(self):
        """получает среднюю зарплату по вакансиям"""
        conn = self.bd()
        try:
            with conn.cursor() as cur:
                # формируем запрос
                cur.execute(f"select  Vacancy.name, avg(Vacancy.salary_from) as salary_from, avg(Vacancy.salary_to) as salary_to "
                            "from vacancy "
                            "GROUP BY Vacancy.name")
                reqest = cur.fetchall()

        except:
            raise
        finally:
            conn.close()

        return reqest

    def get_vacancies_with_higher_salary(self):
        """получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        conn = self.bd()
        try:
            with conn.cursor() as cur:
                # формируем запрос
                cur.execute(f"select  Vacancy.name, Employer.employer_name, Vacancy.salary_from, Vacancy.salary_to "
                            "from vacancy Join employer USING (id_employer) "
                            "Where Vacancy.salary_from > (select avg(salary_from) from vacancy )")
                reqest = cur.fetchall()

        except:
            raise
        finally:
            conn.close()

        return reqest

    def get_vacancies_with_keyword(self, ):
        """получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”"""
        conn = self.bd()
        try:
            with conn.cursor() as cur:
                # формируем запрос
                cur.execute(f"select  Vacancy.name, Employer.employer_name, Vacancy.salary_from, Vacancy.salary_to "
                            "from vacancy Join employer USING (id_employer) "
                            "Where Vacancy.salary_from > (select avg(salary_from) from vacancy )")
                reqest = cur.fetchall()

        except:
            raise
        finally:
            conn.close()

        return reqest