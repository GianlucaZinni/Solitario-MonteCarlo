# El NeoSolitario 
![Cartas de Poker](https://fotos.perfil.com/2022/12/28/trim/950/534/cartas-de-truco-y-poker-20221228-1481314.jpg)

# Índice

1-[Descripción del Proyecto](#Descripción-del-Proyecto) 

A-[Objetivo del proyecto](#Objetivo-del-proyecto) 

B-[Marco teórico](#Marco-teórico) 

I-[Aplicación del método de montecarlo](#Aplicación-del-método-de-montecarlo) 

II-[Aplicación de asignatura de sistemas concurrentes](#Aplicación-de-asignatura-de-sistemas-concurrentes)

C-[El juego:El solitario](#El-juego-El-solitario) 

2- [Estado del proyecto](#Estado-del-proyecto)

3-[Demostración de funciones y aplicaciones](#Demostración-de-funciones-y-aplicaciones)

4-[Acceso al proyecto](#Acceso-al-proyecto)

5-[Tecnologías utilizadas](#Tecnologías-utilizadas)

6-[Personas desarrolladoras del proyecto](#Personas-desarrolladoras-del-proyecto)


## Descripción del Proyecto

### Objetivo del proyecto
<p align="justify">
  El siguiente trabajo de investigación busca comprender y complementar los conocimientos adquiridos en las materias de: “Modelos y Simulación” y “Sistemas Concurrentes”. El objetivo es crear, al final del cuatrimestre, un programa en Python que logre cumplir con los estándares requeridos en ambas asignaturas. Este programa, será la simulación del juego “El Solitario” con sus reglas y patrones básicos. Por un lado en “Modelos y Simulación” se busca plasmar la capacidad de aplicación del método Monte Carlo en el juego para poder tener un mejor aprendizaje y conocimiento del funcionamiento de esta simulación; mientras que por otro lado, el objetivo para “Sistemas Concurrentes” es lograr la correcta integración de los métodos concurrentes de programación, junto con la demostración de las ventajas en rendimiento que esto conlleva.
En este informe planteamos las bases del proyecto El NeoSolitario, en el cual utilizaremos el conocido juego “Solitario”, para poder implementar tanto el Método de Monte Carlo, como la programación de hebras en Python.
</p>

### Marco teórico

#### Aplicación del método de montecarlo
<p align="justify">
Monte Carlo
  Según el gigante tecnológico IBM; “La simulación Monte Carlo o simulación de probabilidad múltiple, es una técnica matemática que se utiliza para estimar los posibles resultados de un evento incierto. El método Monte Carlo fue inventado por John von Neumann y Stanislaw Ulam durante la Segunda Guerra Mundial para mejorar la toma de decisiones en condiciones inciertas.” Este método se puede aplicar en muchos campos de estudio, han evaluado el impacto del riesgo en muchos escenarios de la vida real, como la inteligencia artificial, los precios de acciones, la previsión de ventas, la gestión de proyectos y la fijación de precios. También proporcionan una serie de ventajas sobre los modelos predictivos con entradas fijas, como la capacidad de realizar análisis de sensibilidad o calcular la correlación de entradas. El análisis de sensibilidad permite a los tomadores de decisiones ver el impacto de las entradas individuales en un resultado específico y la correlación les permite comprender las relaciones entre cualquier variable de entrada.
Pero a su vez dentro de las áreas de aplicación, se incluye el juego, dado que el método de Monte Carlo es una técnica de simulación numérica que se utiliza para estimar la probabilidad de un resultado en un evento incierto y complejo mediante la realización de múltiples simulaciones aleatorias. Por ejemplo, se puede utilizar para simular un gran número de partidas en un juego de cartas y estimar la probabilidad de ganar la partida utilizando diferentes estrategias.
Para aplicar el método de Monte Carlo en nuestro juego, se deberán generar varias distribuciones aleatorias de las cartas y se ejecutarán a su vez, varias partidas utilizando diferentes estrategias en cada distribución. Para cada estrategia y cada distribución de cartas, se registra si se gana o pierde la partida. Luego se utiliza la estadística para estimar la probabilidad de éxito promedio para cada estrategia. Esto se logra dividiendo la cantidad total de victorias por la cantidad de partidas jugadas de la misma estrategia.
</p>

#### Aplicación de asignatura de sistemas concurrentes
<p align="justify">
  Para lograr contextualizar la aplicación de la concurrencia en el proyecto, es fundamental primero que todo definir lo que es la concurrencia, junto con ¿Qué es un “Hilo” o “Hebra”?. Empezando por el concepto de  “concurrencia”; este mismo hace referencia a dos o más sucesos que ocurren a la vez y está relacionado con el estudio de las interacciones que subyacen dentro de las actividades concurrentes. Por otro lado, un “hilo” o “thread” es la mínima porción de un programa que puede ser administrada individualmente por el Scheduler. Un programa debe tener como mínimo una hebra y puede tener una o más de ellas (trabajando de manera tanto secuencial como concurrente). El objetivo de utilizar hebras es que cada una tenga tareas determinadas que cumplir, compartiendo recursos y trabajando en sincronización con las demás. De esta manera, permite dividir los procesamientos en varios segmentos de código, dando la posibilidad al programa de ser más eficiente en cuanto a la velocidad de respuesta. 
El objetivo de aplicar este conocimiento a nuestro juego, es poder ejecutar varias partidas al mismo tiempo, permitiendo obtener resultados más rápidos para nuestras estadísticas en cuanto a la eficiencia del programa.  
</p>

## El juego El solitario
<p align="justify">
  A continuación vamos a explicar cuáles son las reglas básicas del Solitario que se implementarán en nuestra aplicación. Teniendo en cuenta las mismas, crearemos una lista de aquellas estrategias de resolución más utilizadas por los jugadores mundialmente. Como dijimos anteriormente, la idea es cumplir con estas estrategias, implementándolas siguiendo un orden de prioridad individual y así comprobar cuál es la mejor para cumplir y terminar el juego de manera óptima en cuanto a movimientos y tiempo de resolución. 
  El Solitario es un juego de cartas de un solo jugador en el que el objetivo es ordenar todas las cartas en cuatro montones separados, uno para cada palo, en orden ascendente desde el As hasta el Rey. Si bien existen muchas variantes del juego, las reglas básicas que aplicaremos en nuestra versión son:
Disposición inicial: se colocan 28 cartas en una mesa en siete columnas. La primera columna tiene una carta, la segunda tiene dos cartas y así sucesivamente hasta que la séptima columna tiene siete cartas. La carta superior de cada columna está boca arriba, mientras que las demás están boca abajo. El resto de cartas quedan dentro del “mazo de reserva” a un costado.
Movimientos: se puede mover una carta a una columna vacía o a otra columna con una carta de valor inmediatamente superior y de un palo diferente. Por ejemplo, un cinco de corazones puede moverse a un seis de tréboles. Se pueden mover varias cartas a la vez si están en orden descendente y de palos alternos. Por ejemplo, un rey de corazones puede moverse a una columna que tenga una dama de espadas.
Cartas boca abajo: cuando una carta boca abajo es la carta superior de una columna y se mueve, se da la vuelta a la siguiente carta.
El mazo de reserva: aquí se ponen todas las cartas que no han sido dispuestas en el tablero. Pueden ser llamadas a juego para construir secuencias para desvelar las cartas ocultas.
El mazo de descarte: este mazo está compuesto por las cartas removidas del mazo de reserva que no han sido posicionadas en el tablero.
Espacio vacío: cuando una columna se queda vacía, solo se puede mover un rey o un grupo de cartas que empiezan por un rey a esa columna.
Ganar: el juego se gana cuando todas las cartas están ordenadas en los cuatro montones de los cuatro palos existentes.
Perder: si no hay más movimientos posibles y no se han ordenado todas las cartas en los montones de palos, se pierde el juego.
</p>

## Estado del proyecto
<p align="justify">
80%/100% 
  Nos encontramos ajustando algunas configuraciones para el correcto funcionamiento de la base de datos. En cuanto al juego como tal, es capaz de jugar por sí solo y gestionar la concurrencia de varias partidas a la vez, quedando pendiente únicamente el manejo de estratégias específicas y la recolección de los datos obtenidos para obtener las estadísticas apropiadas que acompañen a la justificación del uso del método Monte Carlo en esta implementación.
</p>

## Demostración de funciones y aplicaciones
Modo general de qué funciones hay y qué objetivos cumple cada una de ellas

## Acceso al proyecto
1. Para poder descargar el repositorio se deberá ejecutar el siguiente comando en el cmd dentro de la carpeta en la que se desea descargar:
- `git clone https://github.com/GianlucaZinni/Solitario-MonteCarlo.git`
2. Luego se deberá ejecutar el siguiente comando:
- `pip install -r requirements.txt`
3. Por último, si se quiere ejecutar el programa, se deberá correr el siguiente comando
- `python main.py`

## Tecnologías utilizadas
Se ha decidido utilizar ciertas tecnologías específicas para cumplir con los diferentes necesidades del proyecto. 
Lenguaje de programación: python3
Base de datos: MySQL
Librería para el multiprocesamiento: concurrent.futures

## Personas desarrolladoras del proyecto
Juan Pablo Arano
Sebastian Portillo
Sofía Alejandra Prieto
Gianluca Zinni
Bajo la cautelosa tutela y acompañamiento de los profesionales: Claudio Marcelo Menal y Mariano Cosentino.
