from requests import get, post, put, delete
import json
import psycopg2
import data.API_connect

list = []
def get_vacancies():
    url ='https://api.hh.ru/vacancies' # запрос вакансий HH
    vacancy = input (f'введите искомую вакансию \n')
    page =0
    # Справочник для параметров GET-запроса
    par = {
        'text': vacancy, # Текст фильтра. В имени должно быть слово job_title
        'area': '1', # Поиск ощуществляется по вакансиям htubjyf 113 (1 - город Москва)
        'per_page': '20', # Кол-во вакансий на 1 странице
        'page': page # Индекс страницы поиска на HH
           }

    req = get(url, params=par)  # Посылаем запрос к API
    data = req.json()  # Декодируем его ответ, чтобы Кириллица отображалась корректно
    # проверка на наличие данных на странице
    try:
        if  data.get('items',{})[0].get('id') is not None:
            list.append(data)
    except:
        pass
    req.close()

    return list

print (get_vacancies())

data.API_connect.HeadHunterAPI.create_postgres()

# Создаем подключение к PosgrySQL
# conn = psycopg2.connect(host='localhost', user='postgres', password='171717')
#
# # включаем автоматическое сохранение изменений в БД
# conn.autocommit = True
# data_base_name = 'base'
#
# try:
#     with conn.cursor() as cur:
#         # проверка на наличе БД с требуемым именем
#         exists = cur.execute(f"SELECT COUNT(*) = 0 FROM pg_catalog.pg_database WHERE datname = '{data_base_name}'")
#         # если такой БД нет мы ее создаем
#         if not exists:
#             cur.execute(f'CREATE DATABASE  "{data_base_name}"')
#
# except:
#     raise
# finally:
#     conn.close()
