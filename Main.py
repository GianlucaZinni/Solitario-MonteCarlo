import Game
import concurrent.futures
import random
import time

def main():
    num_tareas = 10
    resultados = []

    # Utiliza un ThreadPoolExecutor para manejar los hilos de manera eficiente
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Iniciar todas las tareas y guardar los objetos Future
        futures = [executor.submit(Game, i) for i in range(num_tareas)]

        # Esperar a que las tareas se completen y recolectar los resultados
        for future in concurrent.futures.as_completed(futures):
            try:
                print(f"La tarea {future} fue completada")
            except Exception as e:
                print(f"Error en la tarea: {e}")

    print(f"Se completaron {len(resultados)} tareas.")

if __name__ == "__main__":
    main()
