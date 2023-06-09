import multiprocessing
from static.Database import MySQLConnection
from conf.Game import Game
import sys, random

def play_game(ejecucion, idEstrategia):
    ejecucion += 1
    print(f"Iniciando ejecución {ejecucion}")
    game = Game(ejecucion, idEstrategia)
    print(game.results)
    # game.deck.reset_deck()  # Restablecer el mazo antes de comenzar la partida

    game.game_loop()
    
    insert_results(db_config, game.results)

    print(f"Partida {ejecucion} finalizada")
    if game.finish:
        quit()

# Utilizacion de la base de datos para insertar miles de resultados a la vez
def insert_results(db_config, results):
    with MySQLConnection() as cnx:
        with cnx.cursor() as cursor:
            insert_query = "INSERT INTO games (victoria, duracion, movimientos, mazo, idEstrategia) VALUES (%s, %s, %s, %s, %s)"
            cursor.executemany(insert_query, [(result.victoria, result.duracion, result.movimientos, results.mazo, results.idEstrategia) for result in results])
            cnx.commit()

def main():
    task_quantity = 3  # Cantidad de procesos que se ejecutarán (siempre serán MÍNIMO 3)
    batch_size = 1  # Cantidad de procesos que se ejecutan a la vez. (Tener cuidado con la memoria RAM)
    result_queue = multiprocessing.Queue()
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
    for i in range(0, task_quantity, batch_size):
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

            process = multiprocessing.Process(target=play_game, args=(i, idEstrategia, result_queue))
            processes.append(process)
            process.start()

        # Esperar a que los procesos terminen en el orden correcto
        for process in processes:
            process.join()

if __name__ == "__main__":
    main()
    sys.exit()
