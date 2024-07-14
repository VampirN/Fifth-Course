import psycopg2


class DBManager:
    def __init__(self, host: str, dbname: str, user: str, password: str, port: int):
        self.host = host
        self.dbname = dbname
        self.user = user
        self.password = password
        self.port = port
        self.conn = None
        self.cur = None

    def create_table(self):
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXIST companies (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                url VARCHAR(255) UNIQUE NOT NULL,
                description TEXT
                );
        """)

        cur.execute("""
            CREATE TABLE vacancies (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                url VARCHAR(255) UNIQUE NOT NULL,
                salary TEXT,
                company_id INTEGER REFERENCES companies(id)
                );
                """)

        self.conn.commit()
        cur.close()

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                port=self.port
            )
            self.cur = self.conn.cursor()
            print("Connected to the database")
        except Exception as e:
            print(f"Error connecting to the database: {e}")

    def disconnect(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
        print("Disconnected from the database")

    def get_companies_and_vacancies(self):
        query = ("SELECT c.name, COUNT(v.id) AS vacancies_count "
                 "FROM companies c LEFT JOIN vacancies v ON c.id = v.company_id "
                 "GROUP BY c.name ORDER BY vacancies_count DESC")
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return rows

    def get_all_vacancies(self):
        query = ("SELECT v.name, c.name, v.salary, v.description FROM vacancies v "
                 "JOIN companies c ON v.company_id = c.id ORDER BY v.name")
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return rows

    def get_avg_salary(self):
        query = "SELECT AVG(salary) AS avg_salary FROM vacancies"
        self.cur.execute(query)
        row = self.cur.fetchone()
        return row[0]

    def get_vacancies_with_higher_salary(self, salary):
        query = ("SELECT v.name, c.name, v.salary, v.description FROM vacancies v "
                 "JOIN companies c ON v.company_id = c.id WHERE v.salary > %s ORDER BY v.name")
        self.cur.execute(query, (salary,))
        rows = self.cur.fetchall()
        return rows
