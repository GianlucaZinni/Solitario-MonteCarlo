import mysql.connector
import json

class MySQLConnection:
    def __init__(self):
        with open('static/dbConfig.json', 'r') as f:
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

def read_config():
    with open('static/dbConfig.json') as config_file:
        config = json.load(config_file)
    return config

def create_database():
    # Leer la configuración desde el archivo config.json
    config = read_config()

    # Establecer la conexión a la base de datos
    cnx = mysql.connector.connect(
        host=config['DB_HOST'],
        user=config['DB_USER'],
        password=config['DB_PASSWORD']
    )

    # Verificar si la base de datos existe
    cursor = cnx.cursor()
    cursor.execute("SHOW DATABASES;")
    databases = cursor.fetchall()
    database_exists = False
    for database in databases:
        if config['DB_DATABASE'] in database:
            database_exists = True
            break

    # Si la base de datos no existe, crearla
    if not database_exists:
        cursor.execute("CREATE DATABASE {}".format(config['DB_DATABASE']))
        print("Base de datos '{}' creada.".format(config['DB_DATABASE']))

        # Creación de las tablas correspondientes
        # Leer el archivo SQL
        file_path = "static/CreateSQL.sql"
        with open(file_path, "r") as file:
            sql_script = file.read()

        # Ejecutar el script SQL
        cursor.execute(sql_script, multi=True)
        print("Tablas correspondientes creadas y valores insertados en la tabla Estrategia.")

    # Cerrar el cursor
    cursor.close()
    

def insert_results(results_list):
    # Leer la configuración desde el archivo config.json
    config = read_config()

    # Establecer la conexión a la base de datos
    cnx = mysql.connector.connect(
        host=config['DB_HOST'],
        user=config['DB_USER'],
        password=config['DB_PASSWORD'],
        database=config['DB_DATABASE']
    )

    with cnx.cursor() as cursor:
        insert_query = "INSERT INTO Games (victoria, duracion, movimientos, Mazo, Estrategia_idEstrategia) VALUES (%s, %s, %s, %s, %s)"
        insert_values = []

        for result in results_list:
            duracion_str = result['duracion']
            duracion = int(''.join(filter(str.isdigit, duracion_str)))

            values = (
                result['victoria'],
                duracion,
                result['movimientos'],
                json.dumps(result['mazo']),  # Convertir la lista en una cadena JSON antes de insertarla en la base de datos
                result['idEstrategia']
            )
            insert_values.append(values)

        cursor.executemany(insert_query, insert_values)
        cnx.commit()

    # Cerrar la conexión
    cnx.close()