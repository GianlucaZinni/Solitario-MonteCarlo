# El NeoSolitario 
![Cartas de Poker](https://fotos.perfil.com/2022/12/28/trim/950/534/cartas-de-truco-y-poker-20221228-1481314.jpg)

# Índice

1. [Descripción del Proyecto](#Descripción-del-Proyecto)
   - [Objetivo del proyecto](#Objetivo-del-proyecto)
   - [Marco teórico](#Marco-teórico)
     - [Aplicación del método de montecarlo](#Aplicación-del-método-de-montecarlo)
     - [Aplicación de asignatura de sistemas concurrentes](#Aplicación-de-asignatura-de-sistemas-concurrentes)
   - [El juego:El solitario](#El-juego-El-solitario) 
2. [Estado del proyecto](#Estado-del-proyecto)
3. [Demostración de funciones y aplicaciones](#Demostración-de-funciones-y-aplicaciones)
4. [Acceso al proyecto](#Acceso-al-proyecto)
5. [Tecnologías utilizadas](#Tecnologías-utilizadas)
6. [Personas desarrolladoras del proyecto](#Personas-desarrolladoras-del-proyecto)


## Descripción del Proyecto

### Objetivo del proyecto
<p align="justify">
  El presente trabajo de investigación busca complementar los conocimientos adquiridos en las asignaturas de "Modelos y Simulación" y "Sistemas Concurrentes". El objetivo es desarrollar, al finalizar el cuatrimestre, un programa en Python que cumpla con los estándares requeridos en ambas asignaturas. Este programa será la simulación del juego "El Solitario" respetando sus reglas y patrones básicos. Se buscará implementar el método Monte Carlo para obtener un mejor entendimiento y conocimiento de la simulación; por otro lado, se pretende integrar correctamente los métodos de programación concurrentes, demostrando las ventajas de rendimiento que esto conlleva.
</p>

### Marco teórico

#### Aplicación del método de montecarlo
<p align="justify">
  El método Monte Carlo es una técnica matemática que se utiliza para estimar posibles resultados de un evento incierto mediante la realización de múltiples simulaciones aleatorias. Se puede aplicar en muchos campos de estudio, desde la inteligencia artificial hasta la fijación de precios. Para aplicar el método de Monte Carlo en nuestro juego, se generarán varias distribuciones aleatorias de las cartas y se ejecutarán múltiples partidas utilizando diferentes estrategias en cada distribución. Cada estrategia y cada distribución de cartas registrarán si se gana o pierde la partida. Luego, se utilizará la estadística para estimar la probabilidad de éxito promedio para cada estrategia.
</p>

#### Aplicación de asignatura de sistemas concurrentes
<p align="justify">
  El concepto de concurrencia se refiere a dos o más eventos que ocurren simultáneamente y está relacionado con el estudio de las interacciones que se producen durante las actividades concurrentes. Un hilo o "thread" es la unidad mínima de un programa que puede ser gestionada individualmente por el Scheduler. El objetivo de utilizar hilos es que cada uno tenga tareas específicas para cumplir, compartiendo recursos y trabajando en sincronía con los demás. La aplicación de este conocimiento a nuestro juego nos permitirá ejecutar múltiples partidas al mismo tiempo, obteniendo resultados más rápidos para nuestras estadísticas.
</p>

### El juego: El Solitario
<p align="justify">
  El Solitario es un juego de cartas para un solo jugador en el que el objetivo es ordenar todas las cartas en cuatro montones separados, uno para cada palo, en orden ascendente desde el As hasta el Rey. Las reglas básicas del Solitario que aplicaremos en nuestra versión son las siguientes:
  
- **Disposición inicial**: Se colocan 28 cartas en una mesa en siete columnas. La carta superior de cada columna está boca arriba, mientras que las demás están boca abajo.
- **Movimientos**: Se puede mover una carta a una columna vacía o a otra columna con una carta de valor inmediatamente superior y de un palo diferente. 
- **Cartas boca abajo**: Cuando se mueve la carta superior de una columna que está boca abajo, se da la vuelta a la siguiente carta.
- **El mazo de reserva**: Aquí se ponen todas las cartas que no han sido dispuestas en el tablero. 
- **El mazo de descarte**: Este mazo está compuesto por las cartas removidas del mazo de reserva que no han sido posicionadas en el tablero.
- **Espacio vacío**: Cuando una columna se queda vacía, solo se puede mover un rey o un grupo de cartas que empiecen por un rey a esa columna.
- **Ganar**: El juego se gana cuando todas las cartas están ordenadas en los cuatro montones de los cuatro palos existentes.
- **Perder**: Se pierde el juego si no hay más movimientos posibles y no se han ordenado todas las cartas en los montones de palos.

</p>

## Estado del proyecto
<p align="justify">
  El proyecto se encuentra en un 80% de su desarrollo. Nos encontramos ajustando algunas configuraciones para el correcto funcionamiento de la base de datos. Respecto al juego como tal, es capaz de jugar de manera autónoma y gestionar la concurrencia de varias partidas al mismo tiempo. Queda pendiente el manejo de estrategias específicas y la recolección de los datos obtenidos para proporcionar las estadísticas adecuadas que justifiquen el uso del método Monte Carlo en esta implementación.
</p>

## Demostración de funciones y aplicaciones
*Próximamente.*

## Acceso al proyecto
1. Para clonar el repositorio, ejecutar el siguiente comando en la terminal, en la carpeta donde se desea descargar el proyecto:
- `git clone https://github.com/GianlucaZinni/Solitario-MonteCarlo.git`
2. Se debera crear la base de datos en MySQL con el siguiente codigo:
- `CreateSQL.sql`
3. Instalar las dependencias del proyecto con el siguiente comando:
- `pip install -r requirements.txt`
4. Para ejecutar el programa, correr el siguiente comando:
- `python main.py`

## Tecnologías utilizadas
Para el desarrollo de este proyecto se han utilizado las siguientes tecnologías:

- Lenguaje de programación: Python3
- Base de datos: MySQL
- Librería para el multiprocesamiento: concurrent.futures

## Personas desarrolladoras del proyecto
- Juan Pablo Arano
- Sebastián Portillo
- Sofía Alejandra Prieto
- Gianluca Zinni

Este proyecto se realiza bajo la guía y supervisión de los profesionales Claudio Marcelo Menal y Mariano Cosentino.
