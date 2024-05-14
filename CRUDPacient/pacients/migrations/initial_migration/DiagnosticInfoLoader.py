import pandas as pd
from Connection import Connection
import os

# Ruta al archivo Excel
current_directory = os.path.dirname(os.path.abspath(__file__))
excel_file =  os.path.join(current_directory, "Diagnostico.xlsx")

try:
    # Conexión a la base de datos
    conn = Connection.get_connection()
    cursor = Connection.get_cursor()

    # Leer el archivo Excel
    df = pd.read_excel(excel_file)

    # Eliminar las primeras 5 filas que no son de interés
    diagnostics = df.iloc[6:]

    diagnostics.columns = ['cod_3', 'desc_3', 'cod_4','desc_4']

    father = ""
    disease = ""

    for index, row in diagnostics.iterrows():
        if not pd.isna(row['cod_3']):
            father = row['cod_3']
        else:
            row['cod_3'] = father

        if not pd.isna(row['desc_3']):
            disease = row['desc_3']
        else:
            row['desc_3'] = disease

    for index, row in diagnostics.iterrows():
        cod_3 = row['cod_3']
        desc_3 = row['desc_3']
        cod_4 = row['cod_4']
        desc_4 = row['desc_4']
        
        sql_insert = "INSERT INTO Diagnostico (cod_3, desc_3,cod_4,desc_4) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql_insert, (cod_3,desc_3,cod_4,desc_4))

    # Confirmar la operación
    conn.commit()

    # Cerrar la conexión
    cursor.close()
    conn.close()

except FileNotFoundError:
    print(f"El archivo {excel_file} no fue encontrado.")

except Exception as e:
    print(f"Ocurrió un error: {e}")