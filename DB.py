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

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cnx.close()
