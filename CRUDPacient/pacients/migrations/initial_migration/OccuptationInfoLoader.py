import pandas as pd
from Connection import Connection
import os

# Ruta al archivo Excel
current_directory = os.path.dirname(os.path.abspath(__file__))
excel_file =  os.path.join(current_directory, "Ocupaciones.xlsx")

try:
    # Conexión a la base de datos
    conn = Connection.get_connection()
    cursor = Connection.get_cursor()

    # Leer el archivo Excel
    df = pd.read_excel(excel_file)

    # Eliminar las primeras 5 filas que no son de interés
    ocupations = df.iloc[2:647]

    # Renombrar las columnas para mayor claridad
    ocupations.columns = ['codigo', 'Descripcion', 'Padre']

    # Insertar los datos en la tabla Ciudad
    for index, row in ocupations.iterrows():
        codigo = row['codigo']
        des = row['Descripcion']
        padre = row['Padre']
        
        # Comprobar si el valor de 'Padre' es NaN
        if pd.isna(padre):
            padre = None
        
        sql_insert = "INSERT INTO ocupacion (codigo, descripcion, codigo_padre) VALUES (%s, %s, %s)"
        cursor.execute(sql_insert, (codigo, des, padre))
    
    # Confirmar la operación
    conn.commit()

    # Cerrar la conexión
    cursor.close()
    conn.close()

except FileNotFoundError:
    print(f"El archivo {excel_file} no fue encontrado.")

except Exception as e:
    print(f"Ocurrió un error: {e}")
