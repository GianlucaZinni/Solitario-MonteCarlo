from static.Database import MySQLConnection
import pandas as pd
import matplotlib.pyplot as plt

def fetch_data():

    # Establecer la conexión a la base de datos
    with MySQLConnection() as db:
        conn = db.cnx

        # Ejecutar la consulta SQL para obtener los datos de la tabla Games
        query = "SELECT Estrategia.Nombre AS estrategia, " \
                "CASE WHEN Games.victoria THEN 1 ELSE 0 END AS victoria, " \
                "Games.duracion " \
                "FROM Games " \
                "INNER JOIN Estrategia ON Games.Estrategia_idEstrategia = Estrategia.idEstrategia"
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()

        # Obtener los nombres de las columnas
        columns = [column[0] for column in cursor.description]

        # Crear un DataFrame a partir de los resultados y las columnas
        df = pd.DataFrame.from_records(results, columns=columns)

        # Cerrar el cursor (se cierra automáticamente al salir del contexto "with")
        cursor.close()

    return df



def plot_victory_by_strategy(df):
    victory_count = df.groupby(['estrategia', 'victoria']).size().unstack(fill_value=0)
    victory_count['1'] = victory_count[1]  # Renombrar la columna 1 a '1'
    victory_count = victory_count.drop(columns=[0, 1])  # Eliminar las columnas 0 y 1
    victory_count = victory_count.sort_values(by='1', ascending=False)  # Ordenar por la columna '1'
    victory_count.plot(kind='bar', stacked=True)
    plt.title("Victorias por estrategia")
    plt.xlabel('Estrategia')
    plt.ylabel('Cantidad de victorias')
    plt.show()


def plot_duration_by_strategy(df):
    duration_avg = df.groupby('estrategia')['duracion'].mean()
    duration_avg.plot(kind='bar')
    plt.title("Duración promedio por estrategia")
    plt.xlabel('Estrategia')
    plt.ylabel('Duración promedio')
    plt.show()


def plot_victory_percentage_by_strategy(df):
    victory_percentage = df.groupby('estrategia')['victoria'].mean() * 100
    victory_percentage.plot(kind='bar')
    plt.title("Porcentaje de victoria por estrategia")
    plt.xlabel('Estrategia')
    plt.ylabel('Porcentaje de victoria')
    plt.show()