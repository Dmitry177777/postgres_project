"""Скрипт для заполнения данными таблиц в БД Postgres."""
import psycopg2
# connect to db
import csv

conn = psycopg2.connect(host='localhost', database = 'north', user = 'postgres', password='171717')
try:
    with conn:
        with conn.cursor() as cur:
            # execute query
            with open('north_data\customers_data.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    cur.execute("INSERT INTO customers VALUES (%s, %s, %s)",
                                (row['customer_id'], row['company_name'], row['contact_name']))

    with conn:
        with conn.cursor() as cur:
            # execute query
            with open('north_data\employees_data.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                i=1 # счетчик id
                for row in reader:
                    cur.execute("INSERT INTO employees VALUES (%s, %s, %s, %s, %s, %s)",
                                (i, row['first_name'], row['last_name'], row['title'], row['birth_date'], row['notes']))
                    i+=1
    with conn:
        with conn.cursor() as cur:
            # execute query
            with open('north_data\orders_data.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                i = 1  # счетчик id
                for row in reader:
                    cur.execute("INSERT INTO orders VALUES ( %s, %s, %s, %s, %s)",
                                (row['order_id'], row['customer_id'], row['employee_id'], row['order_date'], row['ship_city']))
                    i += 1


finally:
    conn.close()



