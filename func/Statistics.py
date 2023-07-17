from static.Database import MySQLConnection
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

def fetch_data():

    # Establecer la conexión a la base de datos
    with MySQLConnection() as db:
        conn = db.cnx

        # Ejecutar la consulta SQL para obtener los datos de la tabla Games
        query = "SELECT Estrategia.Nombre AS estrategia, " \
                "CASE WHEN Games.victoria THEN 1 ELSE 0 END AS victoria, " \
                "Games.duracion, " \
                "Games.movimientos " \
                "FROM Games " \
                "INNER JOIN Estrategia ON Games.Estrategia_idEstrategia = Estrategia.idEstrategia"
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()

        # Obtener los nombres de las columnas
        columns = [column[0] for column in cursor.description]

        # Crear un DataFrame a partir de los resultados y las columnas
        df = pd.DataFrame.from_records(results, columns=columns)

        # Calcular la media de movimientos por victorias agrupados por estrategia
        media_movimientos = df.groupby(['estrategia', 'victoria'])['movimientos'].mean()

        # Reiniciar el índice del resultado y convertirlo en DataFrame
        media_movimientos_df = media_movimientos.reset_index()

        # Fusionar los datos calculados con el DataFrame original 'df'
        df = pd.merge(df, media_movimientos_df, on=['estrategia', 'victoria'], how='left')
        df = df.rename(columns={'movimientos_x': 'movimientos', 'movimientos_y': 'media_movimientos'})
        df['simulacion'] = range(1, len(df) + 1)

        # Cerrar el cursor (se cierra automáticamente al salir del contexto "with")
        cursor.close()

    return df



def plot_victory_by_strategy(df):
    victory_count = df.groupby(['estrategia', 'victoria']).size().unstack(fill_value=0)
    total_count = victory_count.sum(axis=1)
    victory_percentage = (victory_count[1] / total_count) * 100
    defeat_percentage = (victory_count[0] / total_count) * 100

    # Ordenar por la tasa de victorias
    sorted_indices = victory_percentage.sort_values(ascending=False).index
    sorted_victory_percentage = victory_percentage.reindex(sorted_indices)
    sorted_defeat_percentage = defeat_percentage.reindex(sorted_indices)

    # Crear el gráfico
    ax = pd.DataFrame({'Victoria': sorted_victory_percentage, 'Derrota': sorted_defeat_percentage}).plot(kind='bar', stacked=True, color=['green', 'red'])
    plt.title("Tasa de victorias y derrotas por estrategia")
    plt.xlabel('Estrategia')
    plt.ylabel('Porcentaje')
    plt.legend(title='Resultado')
    
    plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(5))
    
    plt.xticks(rotation=0)
    
    # Mostrar el porcentaje real en cada barra
    for p in ax.patches:
        percentage = f"{p.get_height():.1f}"
        x_position = p.get_x() + p.get_width() / 2
        y_position = p.get_height() - 3 if p.get_height() > 6 else p.get_height() + 1
        ax.text(x_position, y_position, percentage + '%', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.show()

def plot_duration_by_strategy(df):
    duration_avg = df.groupby('estrategia')['duracion'].mean()

    plt.figure(figsize=(10, 6))  # Ajustar el tamaño del gráfico

    # Crear el gráfico de barras
    ax = duration_avg.plot(kind='bar', color='blue', width=0.6)
    
    plt.title("Duración promedio por estrategia")
    plt.xlabel('Estrategia')
    plt.ylabel('Duración promedio (segundos)')
    
    # Definir un formato para el eje y para mostrar los valores de duración
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.2f}"))

    # Establecer la ubicación y los intervalos de las etiquetas del eje x
    plt.xticks(rotation=0)
    
    # Mostrar las etiquetas de duración sobre cada barra
    for p in ax.patches:
        duration = p.get_height()
        x_position = p.get_x() + p.get_width() / 2
        y_position = p.get_height() + 0.1  # Ajustar la posición vertical del texto
        ax.text(x_position, y_position, f"{duration:.5f}", ha='center', fontsize=10, fontweight='bold')
    
    plt.show()

def plot_percentage_by_strategy_of_total_wins(df):
    victory_percentage = df.groupby('estrategia')['victoria'].mean() * 100
    plt.figure(figsize=(8, 8))  # Tamaño del gráfico de torta
    plt.pie(victory_percentage, labels=victory_percentage.index, autopct='%1.1f%%', startangle=90)
    plt.title("Porcentaje por estrategia del total de victorias")
    plt.show()
    
def plot_mean_moves_by_victory(df):
    mean_moves = df.groupby(['estrategia', 'victoria'])['movimientos'].mean().unstack()
    mean_moves.plot(kind='bar', color=['red', 'green'])
    plt.title("Media de movimientos por victorias para cada estrategia")
    plt.xlabel('Estrategia')
    plt.ylabel('Media de movimientos')
    plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(5))
    plt.legend(['Derrota', 'Victoria'], title='Resultado')
    plt.xticks(rotation=0)
    plt.show()
    

def plot_scatter_duration_movements(df):
    # Obtener una lista de estrategias únicas y asignar un color a cada una
    unique_strategies = df['estrategia'].unique()
    colors = plt.cm.tab10.colors[:len(unique_strategies)]

    # Crear los subgráficos para cada estrategia
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))

    # Crear un gráfico de dispersión para cada estrategia en su subgráfico correspondiente
    for i, strategy in enumerate(unique_strategies):
        strategy_data = df[df['estrategia'] == strategy]
        row = i // 2
        col = i % 2

        # Gráfico de dispersión para victorias (color verde)
        victories_data = strategy_data[strategy_data['victoria'] == 1]
        axs[row, col].scatter(victories_data['duracion'], victories_data['movimientos'], label='Victorias', color='green', marker='x')

        # Gráfico de dispersión para derrotas (color rojo con transparencia)
        defeats_data = strategy_data[strategy_data['victoria'] == 0]
        axs[row, col].scatter(defeats_data['duracion'], defeats_data['movimientos'], label='Derrotas', color='red', marker='o', alpha=0.3)

        axs[row, col].set_title(strategy)
        axs[row, col].set_xlabel('Duración (segundos)')
        axs[row, col].set_ylabel('Cantidad de movimientos')
        axs[row, col].grid()
        axs[row, col].legend()

    # Ajustar los espacios entre los subgráficos
    plt.tight_layout()
    plt.show()
    
def plot_duration_histogram(df):
    # Crear el histograma de duración
    num_bins = 20
    plt.hist(df['duracion'], bins=num_bins, color='blue', alpha=0.7)

    # Personalizar el gráfico
    plt.title("Histograma de Tiempo de Duración")
    plt.xlabel("Duración (segundos)")
    plt.ylabel("Frecuencia")
    plt.grid(True)

    # Ajustar el formato de las etiquetas del eje x para mostrar las cifras decimales en segundos
    durations = df['duracion']
    min_duration = np.floor(durations.min() * 100) / 100  # Redondear al mínimo
    max_duration = np.ceil(durations.max() * 100) / 100   # Redondear al máximo
    step = (max_duration - min_duration) / num_bins
    x_ticks = np.arange(min_duration, max_duration + step, step)
    plt.xticks(x_ticks)

    # Mostrar el gráfico
    plt.show()
    
def plot_convergence_line(df):
    # Calcular la tasa de victorias promedio cada 1000 registros
    window_size = 1000
    df['tasa_victorias_rolling'] = df['victoria'].rolling(window_size, min_periods=1).mean()

    # Crear el gráfico de línea de convergencia con marcadores finos
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df.index, df['tasa_victorias_rolling'], marker='.', markersize=1, color='blue', linestyle='-')
    
    # Línea punteada para la tasa de victorias del 50%
    ax.axhline(y=0.5, color='gray', linestyle='--')

    # Personalizar el gráfico
    plt.title("Gráfico de Línea de Convergencia (Tasa de Victorias)")
    plt.xlabel("Registro")
    plt.ylabel("Tasa de Victorias Promedio")
    plt.grid(True)

    # Ajustar el formato de las etiquetas del eje x para que muestren números enteros
    ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))

    # Mostrar una leyenda con la tasa de victorias promedio
    ax.legend(['Tasa de Victorias Promedio'], loc='lower right')

    # Mostrar el gráfico
    plt.show()