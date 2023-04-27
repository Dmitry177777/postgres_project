from requests import get, post, put, delete
import json
import psycopg2
from data.API_connect import Vacancy


vacancy = input (f'введите искомую вакансию \n')
top = int(input (f'введите объем списка вакагнсий \n'))
vac = Vacancy(vacancy, top)
vac.get_vacancies()
