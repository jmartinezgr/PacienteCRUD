import pandas as pd
from Connection import Connection
import os

# Ruta al archivo Excel
current_directory = os.path.dirname(os.path.abspath(__file__))
excel_file =  os.path.join(current_directory, "Ciudades.xlsx")

try:

    # Conexión a la base de datos
    conn = Connection.get_connection()
    cursor = Connection.get_cursor()

    # Leer el archivo Excel
    df = pd.read_excel(excel_file)

    # Eliminar las primeras 5 filas que no son de interés
    df = df.iloc[10:1131]

    # Seleccionar solo las columnas de interés (C, D, E)
    municipios = df.iloc[:, 2:5]

    # Renombrar las columnas para mayor claridad
    municipios.columns = ['codigo', 'nombre', 'tipo']

    # Insertar los datos en la tabla Ciudad
    for index, row in municipios.iterrows():
        codigo = row['codigo']
        nombre = row['nombre']
        tipo = row['tipo']

        sql_insert = "INSERT INTO Ciudad (nombre, codigo_dane, tipo) VALUES (%s, %s, %s)"
        cursor.execute(sql_insert, (nombre, codigo, tipo))
    
    # Confirmar la operación
    conn.commit()

    # Cerrar la conexión
    cursor.close()
    conn.close()

except FileNotFoundError:
    print(f"El archivo {excel_file} no fue encontrado.")

except Exception as e:
    print(f"Ocurrió un error: {e}")
