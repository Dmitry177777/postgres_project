import os
import json
from abc import ABC, abstractmethod
import time
from requests import get, post, put, delete
import psycopg2

class Engine(ABC):
    @abstractmethod
    def get_vacancies(self):
        pass

    @abstractmethod
    def get_page(self, page=0):
        pass
class Vacancy ():
    """"Класс Vacancy"""


    def __init__(self, search_query,top):

        self.search_query =search_query #  поисковый запрос
        self.top = top # количество вакансий для вывода
        self.vacancy = self.get_vacancies()

        pass

    def get_vacancies(self):


        if self.platforms in [1, 3]: # загрузка платформы 1 - "HeadHunter"
            hh_vacancy = HeadHunterAPI(self.search_query,self.top)

            for i in hh_vacancy:
                for ii in i.get('items'):
                    try:
                        self.list.append({
                                "payment_from": int(ii.get("salary", {}).get("from")),  # Сумма оклада от
                                "payment_to": int(ii.get("salary", {}).get("to")),  # Сумма оклада до
                                "currency": ii.get("salary", {}).get("currency"), # Валюта. Список возможных значений:  rub — рубль  uah — гривна  uzs — сум
                                "platforms":"HeadHunter", # платформа ["HeadHunter", "SuperJob"]
                                 "profession":ii.get("name"), # название вакансии
                                 "candidat":ii.get("snippet",{}).get("requirement"), # 	Требования к кандидату
                                 "work": ii.get("snippet",{}).get("responsibility"), # Должностные обязанности
                                 "compensation": ii.get("working_days"), # Условия работы
                                 "profession_url":ii.get("url") # ссылка на вакансию
                                                                   })
                    except:
                       raise


    def __repr__(self):
        return f'Vacancy({self.search_query}, {self.top_n})'

    def __str__(self):
        return f'{self.search_query}, {self.top_n}'




class HeadHunterAPI (Engine):
    """"Класс HeadHunterAPI"""

    def __init__(self, vacancy, top):
        self.vacancy = vacancy
        self.url ='https://api.hh.ru/vacancies'
        self.pages = int(-1 * top // 1 * -1) # кругление количества страниц в большую сторону
        self.list = self.get_vacancies()
        create_postgres()
        pass



    def get_page(self, page = 0):
        """
          метод для получения страницы со списком вакансий.
          Аргументы: page - Индекс страницы, начинается с 0. Значение по умолчанию 0, т.е. первая страница
          """
        # Справочник для параметров GET-запроса
        par = {
            'text': self.vacancy, # Текст фильтра. В имени должно быть слово job_title
            'area': '1', # Поиск ощуществляется по вакансиям htubjyf 113 (1 - город Москва)
            'per_page': '20', # Кол-во вакансий на 1 странице
            'page': page # Индекс страницы поиска на HH
               }

        req = get(self.url, params=par)  # Посылаем запрос к API
        data = req.json()  # Декодируем его ответ, чтобы Кириллица отображалась корректно
        # проверка на наличие данных на странице
        try:
            if  data.get('items',{})[0].get('id') is not None:
                data_page = data
            else:
                data_page = None
        except:
            raise
        finally:
            req.close()
        return data_page



    def get_vacancies(self):
        """переноса агруженных данных в PostgreSQL"""

        for page in range(0, self.pages):

            # Преобразуем текст ответа запроса в справочник Python
            r_page = self.get_page(page)

            # Проверка на наличие данных на странице
            try:
                if r_page is None:
                    break
            except:
                raise

            # Необязательная задержка, но чтобы не нагружать сервисы hh, оставим. 5 сек мы может подождать
            time.sleep(0.5)

        # Создаем первичную базу данных
        conn = psycopg2.connect(host='localhost',  user='postgres', password='171717')
        try:
            with conn:
                with conn.cursor() as cur:
                    # execute query
                    cur.execute("CREATE DATABASE BASE")
                    for row in self.list:
                        cur.execute("INSERT INTO customers VALUES (%s, %s, %s)",
                                    (row['payment_from'], row['payment_to'], row['name']))
        except:
            raise
        finally:
            conn.close()



        print('Вакансии HeadHunter сохранены в файл')
        return json.dumps(self.list, ensure_ascii=False)

    @staticmethod
    def create_postgres():
        """cоздаем базу и структуру данных в PostgreSQL"""

        # Создаем подключение к PosgrySQL

        conn = psycopg2.connect(host='localhost', user='postgres', password='171717')

        # включаем автоматическое сохранение изменений в БД
        conn.autocommit = True
        # название рабочей БД
        data_base_name = 'base'

        try:
            with conn.cursor() as cur:
                # создаем БД если она есть пропускаем этап создания
                cur.execute(f"SELECT COUNT(*) = 0 FROM pg_catalog.pg_database WHERE datname = '{data_base_name}';")
                exists = cur.fetchone()
                if exists:
                    cur.execute(f"CREATE DATABASE {data_base_name};")
        except:
            raise
        finally:
            conn.close()

        conn = psycopg2.connect(dbname=f'{data_base_name}', host='localhost', user='postgres', password='171717')

        try:
            with conn.cursor() as cur:

                # Таблица работодателей

                # 'items': [
                # {
                #'employer': {
                # 'id': '598471',
                # 'name': 'evrone.ru',
                # 'url': 'https://api.hh.ru/employers/598471',
                # 'alternate_url': 'https://hh.ru/employer/598471',
                # 'logo_urls': {'original': 'https://hhcdn.ru/employer-logo-original/479584.png',
                                # '240': 'https://hhcdn.ru/employer-logo/2360189.png',
                                # '90': 'https://hhcdn.ru/employer-logo/2360188.png'},
                # 'vacancies_url': 'https://api.hh.ru/vacancies?employer_id=598471',
                # 'trusted': True
                # },


                cur.execute(f"CREATE TABLE IF NOT EXISTS employer " # создаем таблицу если ее нет
                            f"(id_employer SERIAL PRIMARY KEY,"
                            f"employer_id INTEGER UNIQUE NOT NULL, "
                            f"employer_name CHARACTER VARYING(30), "
                            f"employer_url CHARACTER VARYING(30), "
                            f"employer_vacancies_url CHARACTER VARYING(30), "
                            f"employer_trusted bit " #0,1,null
                            f")")
                conn.commit()  # сохранение изменений в базе

                #Таблица area
                # 'items': [
                # {
                # 'area': {'id': '1', 'name': 'Москва', 'url': 'https://api.hh.ru/areas/1'},
                cur.execute(f"CREATE TABLE IF NOT EXISTS area "  # создаем таблицу если ее нет
                            f"(id_area SERIAL PRIMARY KEY,"
                            f"area_id INTEGER UNIQUE NOT NULL, "
                            f"area_name CHARACTER VARYING(30), "
                            f"area_url CHARACTER VARYING(30) "
                            f")")
                conn.commit()  # сохранение изменений в базе

                # Таблица type
                # 'items': [
                # {
                # 'type': {'id': 'open', 'name': 'Открытая'},
                cur.execute(f"CREATE TABLE IF NOT EXISTS type "  # создаем таблицу если ее нет
                            f"(id_type SERIAL PRIMARY KEY,"
                            f"type_id INTEGER UNIQUE NOT NULL, "
                            f"type_name CHARACTER VARYING(30) "
                            f")")
                conn.commit()  # сохранение изменений в базе

                #Таблица вакансий

                #'items': [
                # {
                # 'id': '79663730',
                # 'premium': False,
                # 'name': 'Python-разработчик (Junior)',
                # 'department': None,
                # 'has_test': False,
                # 'response_letter_required': False,

                # 'salary': {'from': 50000, 'to': 70000, 'currency': 'RUR', 'gross': False},

                # 'address': None,
                # 'response_url': None,
                # 'sort_point_distance': None,
                # 'published_at': '2023-04-26T20:00:18+0300',
                # 'created_at': '2023-04-26T20:00:18+0300',
                # 'archived': False,
                # 'apply_alternate_url': 'https://hh.ru/applicant/vacancy_response?vacancyId=79663730',
                # 'insider_interview': None,
                # 'url': 'https://api.hh.ru/vacancies/79663730?host=hh.ru',
                # 'adv_response_url': None,
                # 'alternate_url': 'https://hh.ru/vacancy/79663730',
                # 'relations': [],

                cur.execute(f"CREATE TABLE IF NOT EXISTS vacancy "  # создаем таблицу если ее нет
                            f"(id_vacancy SERIAL PRIMARY KEY,"
                            f"id INTEGER UNIQUE NOT NULL, "
                            f"name CHARACTER VARYING(30), "
                            f"departament CHARACTER VARYING(30), "
                            f"id_area INTEGER REFERENCES area (id_area), "
                            f"salary_from INTEGER, "
                            f"salary_to INTEGER, "
                            f"salary_currency CHARACTER VARYING(10), "
                            f"salary_gross bit, " #0,1,null
                            f"id_type INTEGER REFERENCES type (id_type), "
                            f"address CHARACTER VARYING(30), "
                            f"response_url CHARACTER VARYING(30), "
                            f"sort_point_distance CHARACTER VARYING(30), "
                            f"published_at CHARACTER VARYING(30), "
                            f"created_at CHARACTER VARYING(30), "
                            f"archived bit, " #0,1,null
                            f"id_employer INTEGER REFERENCES employer (id_employer)"
                            f")")


                conn.commit() # сохранение изменений в базе

        except:
            raise
        finally:
            conn.close()
        pass
