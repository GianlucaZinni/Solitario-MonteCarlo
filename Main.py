from concurrent.futures import as_completed
import threading
from Game import Game
import concurrent.futures
import random
import time

def jugar_partida(n):
    print(f"Iniciando partida {n}")
    game = Game()
    game.game_loop()
    print(f"Partida {n} finalizada")
    return (game.moves, game.score)


def main():
    num_tareas = 1000
    resultados = []

    # Lock de protección ante concurrencia
    lockResultados = threading.Lock()

    # Utiliza un ThreadPoolExecutor para manejar los hilos de manera eficiente
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Iniciar todas las tareas y guardar los objetos Future
        futures = [executor.submit(jugar_partida(i)) for i in range(num_tareas)]

        # Esperar a que las tareas se completen y recolectar los resultados
        for future in as_completed(futures):
                
            """ 
                PENDIENTE: (CBI)
                    Usar lock, editar var_glob resultados; DB...
            """
            num_movidas = future.result()
            print("RESULT (n of moves): ", num_movidas)
            print(f"La tarea {future} fue completada")


    print(f"Se completaron {len(resultados)} tareas.")

if __name__ == "__main__":
    main()
