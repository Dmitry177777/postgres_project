from requests import get, post, put, delete
import json
import psycopg2
from data.API_connect import Vacancy
from data.DBManager import DBManager

#инициализируем начальные данные запроса к API
vacancy = input (f'введите искомую вакансию \n')
top = int(input (f'введите объем списка вакансий \n'))
vac = Vacancy(vacancy, top)
vac.get_vacancies()


# Запускаем класс DBManager и оформляем запросы к созданной БД
req = DBManager ()

"""получает список всех компаний и количество вакансий у каждой компании"""
input (f'\nсписок всех компаний и количество вакансий у каждой компании\n')
for row in req.get_companies_and_vacancies_count():
    print (row)

"""получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию"""
input (f'\nсписок всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию\n')
for row in req.get_all_vacancies():
    print (row)

"""получает среднюю зарплату по вакансиям"""
input (f'\nсреднюю зарплату по вакансиям\n')
for row in req.get_avg_salary():
    print (row)

"""получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
input (f'\nсписок всех вакансий, у которых зарплата выше средней по всем вакансиям\n')
for row in req.get_vacancies_with_higher_salary():
    print (row)

"""получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”"""
input(f'\nсписок всех вакансий, в названии которых содержатся переданные в метод слова, например “python”\n')
keyword = input(f'ведите поисковый запрос\n')
for row in req.get_vacancies_with_keyword(keyword):
    print(row)