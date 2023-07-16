import mysql.connector
import json, sys

class MySQLConnection:
    def __init__(self):
        with open('static/dbConfig.json', 'r') as f:
            config = json.load(f)
        self.host = config.get('DB_HOST', 'localhost')
        self.user = config.get('DB_USER', 'root')
        self.password = config.get('DB_PASSWORD', '')
        self.database = config.get('DB_DATABASE', 'mi_base_de_datos')

    def connect(self):
        self.cnx = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        print("Conexión a la base de datos establecida.")

    def disconnect(self):
        self.cnx.close()
        print("Se ha desconectado la base de datos.")

    def execute_sql_script(self, sql_script, values=None):
        cursor = self.cnx.cursor()
        # Ejecutar el script SQL
        if values:
            cursor.executemany(sql_script, values)
        else:
            cursor.execute(sql_script)
        print("Script SQL ejecutado correctamente.")

        self.cnx.commit()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()


def read_config():
    with open('static/dbConfig.json') as config_file:
        config = json.load(config_file)
    return config


def create_database():
    # Leer la configuración desde el archivo config.json
    config = read_config()

    try:
        # Establecer la conexión a la base de datos
        cnx = mysql.connector.connect(
            host=config['DB_HOST'],
            user=config['DB_USER'],
            password=config['DB_PASSWORD']
        )
        
    except mysql.connector.Error as e:
        if e.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            print('No se pudo establecer la conexión a la base de datos debido a que las credenciales son incorrectas.')
        else:
            print('No se pudo establecer la conexión a la base de datos.')
        sys.exit(1)

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
    with MySQLConnection() as db:
        insert_query = "INSERT INTO Games (victoria, duracion, movimientos, Mazo, Estrategia_idEstrategia) VALUES (%s, %s, %s, %s, %s)"
        insert_values = []

        for result in results_list:
            duracion = float(result['duracion'])

            values = (
                result['victoria'],
                duracion,
                result['movimientos'],
                json.dumps(result['mazo']),  # Convertir la lista en una cadena JSON antes de insertarla en la base de datos
                result['idEstrategia']
            )
            insert_values.append(values)

        db.execute_sql_script(insert_query, insert_values)