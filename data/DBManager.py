import psycopg2
import data.queries


class DBManager:
    """"Класс обработки запросов к созданной БД PostgreSQL"""

    def __init__(self):
        self.base = 'base'  # Название используемой БД
        pass

    def get_companies_and_vacancies_count():
        """получает список всех компаний и количество вакансий у каждой компании"""
        pass

    def get_all_vacancies():
        """получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию"""
        pass

    def get_avg_salary():
        """получает среднюю зарплату по вакансиям"""
        pass

    def get_vacancies_with_higher_salary():
        """получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        pass

    def get_vacancies_with_keyword():
        """получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”"""
        pass