import mysql.connector
import json
class MySQLConnection:
    def __init__(self, host, user, password, database):
        with open('dbConfig.json', 'r') as f:
            config = json.load(f)
        self.host = config.get('DB_HOST', 'localhost')
        self.user = config.get('DB_USER', 'root')
        self.password = config.get('DB_PASSWORD', '')
        self.database = config.get('DB_DATABASE', 'mi_base_de_datos')

    def __enter__(self):
        self.cnx = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        return self.cnx

    def database_exists(self):
        cursor = self.cnx.cursor()
        cursor.execute(f"SHOW DATABASES LIKE '{self.database}'")
        return cursor.fetchone() is not None

    def execute_sql_script(self, file_path):
        with open(file_path, 'r') as file:
            sql_script = file.read()
        statements = sql_script.split(';')

        cursor = self.cnx.cursor()
        for statement in statements:
            if statement.strip():
                cursor.execute(statement)
        self.cnx.commit()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cnx.close()
