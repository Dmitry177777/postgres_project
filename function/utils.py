from requests import get, post, put, delete
import json
import psycopg2
from data.API_connect import Vacancy
from data.DBManager import DBManager

# инициализируем начальные данные запроса к API
# vacancy = input (f'введите искомую вакансию \n')
# top = int(input (f'введите объем списка вакансий \n'))
# vac = Vacancy(vacancy, top)
# vac.get_vacancies()

# Запускаем класс DBManager и оформляем запросы к созданной БД
req = DBManager ()

"""получает список всех компаний и количество вакансий у каждой компании"""
for row in req.get_companies_and_vacancies_count():
    print (row)


