import psycopg2
from psycopg2.extras import RealDictCursor

# Подключение к базе данных
connection = psycopg2.connect(
    dbname="your_database_name", # наименование базы данных
    user="your_username", # логин
    password="your_password", # пароль
    host="localhost" # по умолчанию всегда localhost
)

cursor = connection.cursor(cursor_factory=RealDictCursor)

# Загрузка данных о компаниях
with open('companies.json', 'r') as file:
    companies_data = json.load(file)
    for company in companies_data:
        cursor.execute("""
            INSERT INTO companies (name, url, description)
            VALUES (%(name)s, %(url)s, %(description)s)
        """, company)

# Загрузка данных о вакансиях
with open('vacancies.json', 'r') as file:
    vacancies_data = json.load(file)
    for vacancy in vacancies_data:
        cursor.execute("""
            INSERT INTO vacancies (title, url, salary, company_id)
            VALUES (%(title)s, %(url)s, %(salary)s, %(company_id)s)
        """, vacancy)

connection.commit()
cursor.close()
connection.close()