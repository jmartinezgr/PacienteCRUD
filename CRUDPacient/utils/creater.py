import subprocess
import os
import sys

# Obtiene el directorio actual del script
current_directory = os.path.dirname(os.path.abspath(__file__))
project_directory = os.path.join(os.path.dirname(current_directory),"pacients/migrations/initial_migration")

# Nombre de los scripts a ejecutar
scripts = ['DataBaseCreator.py', 'OccuptationInfoLoader.py', 'CityInfoLoader.py','DiagnosticInfoLoader.py','NationsInfoLoader.py']
desc = ['Base de datos Creada Existosamente','Ocupaciones Cargadas Exitosamente','Ciudades Cargadas Exitosamente','Diagnosticos Cargados Exitosamente','Naciones Cargadas Exitosamente']

try:
    for index in range(len(scripts)):
        # Construye la ruta completa al script
        script_path = os.path.join(project_directory, scripts[index])
        # Ejecuta el script
        subprocess.call(['python', script_path])
        print(desc[index])
    print("Success")
except Exception as e:
    print(f"Error: {e}")
    sys.exit()