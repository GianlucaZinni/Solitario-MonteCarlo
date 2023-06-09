import multiprocessing
from static.Database import MySQLConnection
from conf.Game import Game
import sys, random

def play_game(partida, idEstrategia):
    print(f"Iniciando partida {partida}")
    game = Game(idEstrategia)
    results = game.game_loop()
    print(f"Partida {partida} finalizada")
    return results

# Utilizacion de la base de datos para insertar miles de resultados a la vez
# def insert_results(db_config, results):
#     with MySQLConnection() as cnx:
#         with cnx.cursor() as cursor:
#             insert_query = "INSERT INTO games (victoria, duracion, idEstrategia) VALUES (%s, %s, %s)"
#             cursor.executemany(insert_query, [(result.win, result.duration, result.idEstrategia) for result in results])
#             cnx.commit()

def main():
    task_quantity = 6
    results = []
    batch_size = 2  # Cantidad de procesos que se ejecutan a la vez. (Tener cuidado con la memoria RAM)
    pool = multiprocessing.Pool(processes=batch_size)

    target_count = task_quantity // 3  # Siendo 3 la cantidad de Estrategias
    count_1 = count_2 = count_3 = 0  # Contadores para cada valor
    for i in range(0, task_quantity, batch_size):
        games = []
        for _ in range(i, min(i + batch_size, task_quantity)):
            # Generar un idEstrategia aleatorio que aún no se haya utilizado la cantidad target_count de veces
            idEstrategia = random.choice([1, 2, 3])
            while (idEstrategia == 1 and count_1 >= target_count) or (idEstrategia == 2 and count_2 >= target_count) or (idEstrategia == 3 and count_3 >= target_count):
                idEstrategia = random.choice([1, 2, 3])
            
            # Incrementar el contador correspondiente
            if idEstrategia == 1:
                count_1 += 1
            elif idEstrategia == 2:
                count_2 += 1
            elif idEstrategia == 3:
                count_3 += 1

            games.append(
                pool.apply_async(
                    play_game, (i, idEstrategia,)
                )
            )

        for game in games:
            try:
                result = game.get()
                results.append(result)
                print(results)
                print(f"La tarea {game} fue completada")
            except Exception as e:
                print(f"Error en la partida: {e}")
    print(f"Se completaron {len(results)} tareas.")
    # Ejecucion de funcion que inserta los 1000 resultados en la DB
    # insert_results(results)

if __name__ == "__main__":
    main()
    sys.exit()