import multiprocessing
import sys
import time
import json
import pandas as pd
import matplotlib.pyplot as plt
import psutil
from func.Database import insert_results, create_database
from func.Strategies import fetch_data, plot_victory_by_strategy, plot_duration_by_strategy, plot_victory_percentage_by_strategy 

from conf.Game import Game
from conf.Deck import Deck

strategies_output = {
    1: "El Marino",
    2: "La Socialista",
    3: "El Bombero"
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
    return game.results


def read_config():
    with open('static/dbConfig.json') as config_file:
        config = json.load(config_file)
    return config


def worker(partida, idEstrategia, results_queue):
    result = play_game(partida, idEstrategia)
    results_queue.put(result)


def main(analyze_performance=False):

    if analyze_performance:
        sequential_cpu_time = 0
        sequential_memory_usage = 0

    # Utilizar una cola compartida para almacenar los resultados de los procesos
    manager = multiprocessing.Manager()
    results_queue = manager.Queue()

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

    if analyze_performance:
        # Ejecución secuencial
        sequential_start_time = time.perf_counter()
        sequential_results_list = []
        for partida in range(1, task_quantity + 1):
            idEstrategia = (partida - 1) % 3 + 1
            result = play_game(partida, idEstrategia)
            sequential_results_list.append(result)
        sequential_end_time = time.perf_counter()
        sequential_cpu_time = sequential_end_time - sequential_start_time
        sequential_memory_usage = psutil.Process().memory_info().rss

        parallel_start_time = time.perf_counter()


    for i in range(0, task_quantity, batch_size):
        for _ in range(i, min(i + batch_size, task_quantity)):
            # Generar un idEstrategia que aún no se haya utilizado la cantidad target_count de veces
            idEstrategia = (count_1 + count_2 + count_3) % 3 + 1
            while (idEstrategia == 1 and count_1 >= target_count) or (
                    idEstrategia == 2 and count_2 >= target_count) or (
                    idEstrategia == 3 and count_3 >= target_count):
                idEstrategia = (count_1 + count_2 + count_3) % 3 + 1

            # Incrementar el contador correspondiente
            if idEstrategia == 1:
                count_1 += 1
            elif idEstrategia == 2:
                count_2 += 1
            elif idEstrategia == 3:
                count_3 += 1

            process = multiprocessing.Process(target=worker, args=(partida, idEstrategia, results_queue))
            processes.append(process)
            process.start()
            partida += 1  # Incrementar el valor de x en cada ejecución

    # Esperar a que los procesos terminen en el orden correcto
    for process in processes:
        process.join()

    # Extraer los resultados de la cola
    results_list = []
    while not results_queue.empty():
        result = results_queue.get()
        results_list.append(result)

    # Inserta todos los resultados en la base de datos
    print("RESULTS LIST: ", results_list)
    insert_results(results_list)

    if analyze_performance:
        finish_time = time.perf_counter()
        parallel_cpu_time = finish_time - parallel_start_time
        parallel_memory_usage = psutil.Process().memory_info().rss

        print("\nEjecución paralela:")
        print("Tiempo de CPU: {:.2f} segundos".format(parallel_cpu_time))
        print("Uso de memoria: {:.2f} MB".format(parallel_memory_usage / (1024 * 1024)))
        print("---")
        print("Ejecución secuencial:")
        print("Tiempo de CPU: {:.2f} segundos".format(sequential_cpu_time))
        print("Uso de memoria: {:.2f} MB".format(sequential_memory_usage / (1024 * 1024)))
        print("---")

        # Gráfico de barras para comparar el tiempo de CPU
        labels = ['Paralelo', 'Secuencial']
        cpu_times = [parallel_cpu_time, sequential_cpu_time]
        plt.bar(labels, cpu_times)
        plt.xlabel('Tipo de ejecución')
        plt.ylabel('Tiempo de CPU (segundos)')
        plt.title('Comparación del tiempo de CPU entre ejecuciones paralela y secuencial')
        plt.show()

        # Gráfico de barras para comparar el uso de memoria
        memory_usages = [parallel_memory_usage, sequential_memory_usage]
        plt.bar(labels, memory_usages)
        plt.xlabel('Tipo de ejecución')
        plt.ylabel('Uso de memoria (MB)')
        plt.title('Comparación del uso de memoria entre ejecuciones paralela y secuencial')
        plt.show()


if __name__ == "_main_":
    create_database()
    main(analyze_performance=True)
    df = fetch_data()
    plot_victory_by_strategy(df)
    plot_duration_by_strategy(df)
    plot_victory_percentage_by_strategy(df)
    sys.exit()