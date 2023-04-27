import os
import json
# from abc import ABC, abstractmethod
import time
from requests import get, post, put, delete
import psycopg2


class Vacancy :
    """"Класс HeadHunterAPI"""

    def __init__(self, vacancy, top):
        self.vacancy = vacancy
        self.url = 'https://api.hh.ru/vacancies'
        self.per_page = 20 # количество вакансий на 1 странице
        self.pages = int(-1 * top // self.per_page * -1)  # кругление количества страниц в большую сторону
        self.base = 'base'  # НАзвание используемой БД

        pass



    def get_page(self, page = 0):
        """
          метод для получения страницы со списком вакансий.
          Аргументы: page - Индекс страницы, начинается с 0. Значение по умолчанию 0, т.е. первая страница
          """
        # Справочник для параметров GET-запроса
        par = {
            'text': self.vacancy, # Текст фильтра. В имени должно быть слово job_title
            #'area': '1', # Поиск ощуществляется по вакансиям htubjyf 113 (1 - город Москва)
            'per_page': self.per_page, # Кол-во вакансий на 1 странице
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

        #формируем базу данных и структуру таблиц
        self.create_postgres()


        for page in range(0, self.pages):

            # Преобразуем текст ответа запроса в справочник Python
            r_page = self.get_page(page)

            # Проверка на наличие данных на странице
            try:
                if r_page is None:
                    break
            except:
                raise



            # Поделючаемся к базе данных
            conn = psycopg2.connect(dbname=f'{self.base}', host='localhost', user='postgres', password='171717')

            # Записываем данные страницы в БД
            try:
                with conn.cursor() as cur:
                    for row in r_page.get("items"):
                        print (row)

                        # таблица employer
                        # проверка значения на уникальность
                        cur.execute(f'select count (employer_id) from employer WHERE employer_id = {row.get("employer", {}).get("id")}')
                        unic = cur.fetchone()
                        if unic[0] == 0 :
                            #внесение уникальных записей
                            cur.execute("INSERT INTO employer (employer_id,employer_name, employer_url, employer_vacancies_url, employer_trusted) VALUES (%s, %s, %s, %s, %s)",
                                (row.get("employer", {}).get("id"),
                                 row.get("employer", {}).get("name"),
                                 row.get("employer", {}).get("url"),
                                 row.get("employer", {}).get("vacancies_url"),
                                 '1' if row.get("employer", {}).get("trusted") else '0')) # если True то записываем 1, если False то записываем 0
                        conn.commit()  # сохранение изменений в базе

                        # получение номера pk
                        cur.execute(f"SELECT MAX(id_employer) FROM employer")
                        id_employer_i = cur.fetchone()[0]

                        # таблица area
                        # проверка значения на уникальность
                        cur.execute(f'select count (area_id) from area WHERE area_id = {row.get("area", {}).get("id")}')
                        unic = cur.fetchone()[0]
                        if unic == 0 :
                        # внесение уникальных записей
                             cur.execute("INSERT INTO area (area_id, area_name, area_url) VALUES (%s, %s, %s)",
                                (row.get("area", {}).get("id"),
                                 row.get("area", {}).get("name"),
                                 row.get("area", {}).get("url")))

                        conn.commit()  # сохранение изменений в базе
                        #получение номера pk
                        cur.execute(f"SELECT MAX(id_area) FROM area")
                        id_area_i = cur.fetchone()[0]

                        # таблица type
                        # внесение  записей
                        cur.execute("INSERT INTO type (type_id, type_name) VALUES (%s, %s)",
                            (row.get("type", {}).get("id"),
                             row.get("type", {}).get("name")))

                        conn.commit()  # сохранение изменений в базе
                        # получение номера pk
                        cur.execute(f"SELECT MAX(id_type) FROM type")
                        id_type_i = cur.fetchone()[0]

                        # таблица vacancy
                        # внесение  записей ч.1
                        cur.execute(f"INSERT INTO vacancy "
                            "(id, "
                            "name, "
                            "departament, "
                            "id_area, "
                            "salary_from, "
                            "salary_to, "
                            "salary_currency, "
                            "salary_gross) "
                            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                            (row.get("id"),
                             row.get("name"),
                             row.get("department") or "",
                             id_area_i,
                             row.get("salary", {}).get("from") or 0,
                             row.get("salary", {}).get("to") or 0,
                             row.get("salary", {}).get("currency"),
                             '1' if row.get("salary", {}).get("gross") else '0')) # если True то записываем 1, если False то записываем 0


                        cur.execute(f"INSERT INTO vacancy "
                                    "(id_type, "
                                    "address, "
                                    "response_url, "
                                    "sort_point_distance, "
                                    "published_at, "
                                    "created_at, "
                                    "archived, "
                                    "id_employer) "
                                    "VALUES %s,%s,%s,%s,%s,%s,%s,%s",
                                    (id_type_i,
                                     row.get("address", {}).get("city")+", ул."+row.get("address", {}).get("street")+", д."+row.get("address", {}).get("building") or "",
                                     row.get("response_url") or "",
                                     row.get("sort_point_distance") or "",
                                     row.get("published_at"),
                                     row.get("created_at"),
                                     '1' if row.get("archived") else '0',  # если True то записываем 1, если False то записываем 0,
                                     id_employer_i))


                        conn.commit()  # сохранение изменений в базе

            except AttributeError:
                raise
            finally:
                conn.close()

        # Необязательная задержка, но чтобы не нагружать сервисы hh, оставим. 5 сек мы может подождать
        time.sleep(0.5)

        print('Вакансии HeadHunter сохранены в БД>')
        pass


    def create_postgres(self):
        """cоздаем базу и структуру данных в PostgreSQL"""

        # Создаем подключение к PosgrySQL

        conn = psycopg2.connect(host='localhost', user='postgres', password='171717')

        # включаем автоматическое сохранение изменений в БД
        conn.autocommit = True


        try:
            with conn.cursor() as cur:
                # Если база данных запроса была раньше удалем ее и  создаем новую БД
                cur.execute(f"DROP DATABASE IF EXISTS {self.base} WITH(FORCE)")
                cur.execute(f"CREATE DATABASE {self.base}")
        except:
            raise
        finally:
            conn.close()

        conn = psycopg2.connect(dbname=f'{self.base}', host='localhost', user='postgres', password='171717')

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


                cur.execute(f"CREATE TABLE employer " # создаем таблицу если ее нет
                            f"(id_employer SERIAL PRIMARY KEY,"
                            f"employer_id INTEGER UNIQUE NOT NULL, "
                            f"employer_name CHARACTER VARYING(60), "
                            f"employer_url CHARACTER VARYING(60), "
                            f"employer_vacancies_url CHARACTER VARYING(60), "
                            f"employer_trusted bit " #0,1,null
                            f")")
                conn.commit()  # сохранение изменений в базе

                #Таблица area
                # 'items': [
                # {
                # 'area': {'id': '1', 'name': 'Москва', 'url': 'https://api.hh.ru/areas/1'},
                cur.execute(f"CREATE TABLE area "  # создаем таблицу если ее нет
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
                cur.execute(f"CREATE TABLE type "  # создаем таблицу если ее нет
                            f"(id_type SERIAL PRIMARY KEY,"
                            f"type_id CHARACTER VARYING(30) NOT NULL, "
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

                cur.execute(f"CREATE TABLE vacancy "  # создаем таблицу если ее нет
                            f"(id_vacancy SERIAL PRIMARY KEY,"
                            f"id INTEGER UNIQUE NOT NULL, "
                            f"name CHARACTER VARYING(60), "
                            f"departament CHARACTER VARYING(30), "
                            f"id_area INTEGER REFERENCES area (id_area), "
                            f"salary_from INTEGER, "
                            f"salary_to INTEGER, "
                            f"salary_currency CHARACTER VARYING(10), "
                            f"salary_gross bit, " #0,1,null
                            f"id_type INTEGER REFERENCES type (id_type), "
                            f"address CHARACTER VARYING(30), "
                            f"response_url CHARACTER VARYING(60), "
                            f"sort_point_distance CHARACTER VARYING(30), "
                            f"published_at TIMESTAMP, "
                            f"created_at TIMESTAMP, "
                            f"archived bit, " #0,1,null
                            f"id_employer INTEGER REFERENCES employer (id_employer)"
                            f")")


                conn.commit() # сохранение изменений в базе

        except:
            raise
        finally:
            conn.close()
        pass
