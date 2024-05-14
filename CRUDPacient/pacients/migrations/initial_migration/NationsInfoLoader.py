import pandas as pd
from Connection import Connection
import os

# Ruta al archivo Excel
current_directory = os.path.dirname(os.path.abspath(__file__))
excel_file = os.path.join(current_directory, "paises.xlsx")

try:
    # Conexión a la base de datos
    conn = Connection.get_connection()
    cursor = Connection.get_cursor()

    # Leer el archivo Excel
    df = pd.read_excel(excel_file)

    # Rellenar valores NaN en la columna 'Codigo' con un valor por defecto, por ejemplo, 0
    df['Codigo'].fillna("NA", inplace=True)

    # Insertar los datos en la tabla Ciudad
    for index, row in df.iterrows():
        codigo = row['Codigo']
        nombre = row['Descripcion']
        sql_insert = "INSERT INTO Nacionalidad (id_nacionalidad, nombre) VALUES (%s, %s)"
        cursor.execute(sql_insert, (codigo, nombre))
    
    # Confirmar la operación
    conn.commit()

    # Cerrar la conexión
    cursor.close()
    conn.close()

except FileNotFoundError:
    print(f"El archivo {excel_file} no fue encontrado.")

except Exception as e:
    print(f"Ocurrió un error: {e}")
