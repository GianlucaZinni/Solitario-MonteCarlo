import threading
from DB import MySQLConnection
from Game import Game
import concurrent.futures
import random
import time
import json
import os

def play_game(n):
    print(f"Iniciando partida {n}")
    game = Game()
    results = game.game_loop()
    print(f"Partida {n} finalizada")
    return results

# Funcion que permite configurar la DB con los datos de dbConfig.json
def load_config(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)
    return config

# Utilizacion de la base de datos para insertar miles de resultados a la vez
def insert_results(db_config, results):
    with MySQLConnection(**db_config) as cnx:
        with cnx.cursor() as cursor:
            insert_query = "INSERT INTO nombre_tabla (estrategia, resultado) VALUES (%s, %s)"
            cursor.executemany(insert_query, results)
            cnx.commit()

def main():
    task_quantity = 1000
    results = []

    # Lock de protección ante concurrencia
    lockResultados = threading.Lock()

    # Utiliza un ThreadPoolExecutor para manejar los hilos de manera eficiente
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(play_game, i) for i in range(task_quantity)]
        for future in concurrent.futures.as_completed(futures):
            try:
                resultado = future.result()
                with threading.Lock():
                    results.append(resultado)
                print(f"La tarea {future} fue completada")
            except Exception as e:
                print(f"Error en la partida: {e}")

    print(f"Se completaron {len(results)} tareas.")
    
    # Inicializaacion DB
    config = load_config('dbConfig.json')
    db_config = {
        'host': config.get('DB_HOST', 'localhost'),
        'user': config.get('DB_USER', 'root'),
        'password': config.get('DB_PASSWORD', ''),
        'database': config.get('DB_DATABASE', 'mi_base_de_datos')
    }
    # Ejecucion de funcion que inserta los 1000 resultados en la DB
    insert_results(db_config, results)

if __name__ == "__main__":
    main()
