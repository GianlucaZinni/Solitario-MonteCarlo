import multiprocessing
from static.Database import MySQLConnection
import mysql.connector
from conf.Game import Game
from conf.Deck import Deck
import sys
import time
import json

strategies_output = {
    1 : "El Marino",
    2 : "La Socialista",
    3 : "El Bombero"
}
victory_output = {
    False: "Perdió",
    True: "Ganó"
}

def play_game(partida, idEstrategia):
    deck = Deck()
    deck.shuffle()

    game = Game(partida, idEstrategia, deck)
    game.game_loop()
    results = game.results

    print(f"Partida: {partida} - Estrategia: {strategies_output.get(results.get('idEstrategia'))} finalizada - Resultado: {victory_output.get(results.get('victoria'))}")
    if game.game_is_running is False:
        quit()
    return game.results


# Utilizacion de la base de datos para insertar miles de resultados a la vez
def read_config():
    with open('static/dbConfig.json') as config_file:
        config = json.load(config_file)
    return config

def insert_results(results_list):
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
        # Creación de las tablas correspondientes:
        # Leer el archivo SQL
        file_path = "static/CreateSQL.sql"
        with open(file_path, "r") as file:
            sql_script = file.read()
        # Ejecutar el script SQL
        cursor.execute(sql_script, multi=True)
        # Verificar y avanzar hasta el final de los resultados del cursor
        while cursor.nextset():
            pass
        # Confirmar los cambios
        cnx.commit()
        print("Tablas correspondientes creadas.")

    # Cerrar el cursor
    cursor.close()

    # Establecer una nueva conexión a la base de datos
    cnx = mysql.connector.connect(
        host=config['DB_HOST'],
        user=config['DB_USER'],
        password=config['DB_PASSWORD'],
        database=config['DB_DATABASE']
    )

    with cnx.cursor() as cursor:
        insert_query = "INSERT INTO games (victoria, duracion, movimientos, mazo, idEstrategia) VALUES (%s, %s, %s, %s, %s)"
        insert_values = []
        for results in results_list:
            insert_values.extend([(result['victoria'], result['duracion'], result['movimientos'], result['mazo'], result['idEstrategia']) for result in results])
        cursor.executemany(insert_query, insert_values)
        cnx.commit()

    # Cerrar la conexión
    cnx.close()


# Función que inicia el juego y luego agrega los resultados a results_list
def worker(partida, idEstrategia, results_list):
    result = play_game(partida, idEstrategia)
    results_list.append(result)

    print("WORKER PRINT. RESULT: ", result)


def main(analyze_performance=False):

    if analyze_performance:
        start_time = time.perf_counter()

    # Lista compartida donde cada proceso agrega su resultado
    manager = multiprocessing.Manager()
    results_list = manager.list()

    task_quantity = 1  # Cantidad de procesos que se ejecutarán (siempre serán MÍNIMO 3)
    batch_size = 1  # Cantidad de procesos que se ejecutan a la vez. (Tener cuidado con la memoria RAM)
    processes = []

    if task_quantity < 3:
        task_quantity = 3 
        
    if batch_size <= 0 or batch_size > task_quantity:
        batch_size = task_quantity

    if task_quantity % 3 != 0:
        diferencia = 3 - (task_quantity % 3)  # Calcula la diferencia necesaria para que sea divisible por 3
        if diferencia <= 1.5:
            task_quantity += round(diferencia)  # Suma la diferencia redondeada si es menor o igual a 1.5
        else:
            task_quantity -= round(3 - diferencia)  # Resta la diferencia redondeada si es mayor a 1.5

    target_count = task_quantity // 3  # Siendo 3 la cantidad de Estrategias
    count_1 = count_2 = count_3 = 0  # Contadores para cada valor
    partida = 1  # Variable contador para incrementar en cada ejecución
    for i in range(0, task_quantity, batch_size):
        for _ in range(i, min(i + batch_size, task_quantity)):
            # Generar un idEstrategia que aún no se haya utilizado la cantidad target_count de veces
            idEstrategia = (count_1 + count_2 + count_3) % 3 + 1
            while (idEstrategia == 1 and count_1 >= target_count) or (idEstrategia == 2 and count_2 >= target_count) or (idEstrategia == 3 and count_3 >= target_count):
                idEstrategia = (count_1 + count_2 + count_3) % 3 + 1
            
            # Incrementar el contador correspondiente
            if idEstrategia == 1:
                count_1 += 1
            elif idEstrategia == 2:
                count_2 += 1
            elif idEstrategia == 3:
                count_3 += 1
                
            process = multiprocessing.Process(target=worker, args=(partida, idEstrategia, results_list))
            processes.append(process)
            process.start()
            partida += 1  # Incrementar el valor de x en cada ejecución
            
        # Esperar a que los procesos terminen en el orden correcto
        for process in processes:
            process.join()

    # Inserta todos los resultados en la base de datos    
    insert_results(results_list)

    if analyze_performance:
        finish_time = time.perf_counter()
        print("\n Programa concurrente finalizado en {} segundos".format(finish_time - start_time))
        print("---")


if __name__ == "__main__":
    main(analyze_performance=True) 
    sys.exit()
