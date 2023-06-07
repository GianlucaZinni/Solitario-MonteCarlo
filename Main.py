import multiprocessing
from DB import MySQLConnection
from Game import Game
import sys

def play_game(n):
    print(f"Iniciando partida {n}")
    game = Game()
    results = game.game_loop()
    print(f"Partida {n} finalizada")
    return results

# Utilizacion de la base de datos para insertar miles de resultados a la vez
def insert_results(db_config, results):
    with MySQLConnection() as cnx:
        with cnx.cursor() as cursor:
            insert_query = "INSERT INTO games (victoria, duracion, idEstrategia) VALUES ({results.win}, {results.duration}, {results.idEstrategia})"
            cursor.executemany(insert_query, results)
            cnx.commit()

def main():
    task_quantity = 1
    results = []

    with multiprocessing.Pool(processes=task_quantity) as pool:
        games = [pool.apply_async(play_game, (i,)) for i in range(task_quantity)]
        for game in games:
            try:
                result = game.get()
                results.append(result)
                print(f"La tarea {game} fue completada")
            except Exception as e:
                print(f"Error en la partida: {e}")
    print(f"Se completaron {len(results)} tareas.")
    # Ejecucion de funcion que inserta los 1000 resultados en la DB
    insert_results(results)

if __name__ == "__main__":
    main()
    sys.exit()
