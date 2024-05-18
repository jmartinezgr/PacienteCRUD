# Instrucciones para el uso de la aplicación Django CRUDPaciente

## Requisitos previos

Antes de ejecutar la aplicación, asegúrate de tener lo siguiente:

- **Servidor MySQL:** Se recomienda utilizar XAMPP para gestionar el servidor MySQL. Puedes descargarlo desde [aquí](https://www.apachefriends.org/index.html).
- **Motor de base de datos MySQL:** Debes tener un motor de base de datos MySQL instalado y activo. El usuario utilizado para acceder a la base de datos debe ser `root`.
- **Clave vacía:** No se requiere contraseña para el usuario `root`. Si ya tienes configurado tu motor de bases de datos MySQL con otro usuario y contraseña, puedes modificar la configuración en tu versión local (ver detalles al final del documento).
- **La base de datos debe estar siempre activa:** Asegúrate de que el motor de base de datos MySQL esté siempre en ejecución mientras interactúas con la aplicación Django.
- Tener github instalado
- Tener instaladas las siguientes librerías:
  - [Django](https://www.djangoproject.com/): `pip install django`
  - [PyMySQL](https://pypi.org/project/PyMySQL/): `pip install pymysql`
  - [Openyxl](https://pypi.org/project/openpyxl/): `pip install openpyxl`
  - [Pandas](https://pypi.org/project/pandas/): `pip install pandas`

O puedes Ejecutar este comando para instalarlas todas
```bash
pip install django pymysql openpyxl pandas
```
## Pasos para la configuración

Sigue estos pasos para configurar y ejecutar la aplicación:

1. Clona el repositorio de GitHub utilizando el siguiente enlace:

```bash
git clone https://github.com/jmartinezgr/PacienteCRUD.git
cd PacienteCRUD
```

2. Una vez clonado el repositorio, asegúrate de tener disponible la base de datos mencionada anteriormente.
3. Navega al directorio `CRUDPacient/utils` en la terminal:

```bash
cd CRUDPacient/utils
python creator.py
```

Si obtienes una respuesta como esta:

```bash
Base de datos Creada Existosamente
Ocupaciones Cargadas Exitosamente
Ciudades Cargadas Exitosamente
Diagnosticos Cargados Exitosamente
Naciones Cargadas Exitosamente
Success
```

Sabras que todas las tablas e informacion basica de la aplicacion ha sido cargada a tu base de datos MySQL y esta listo para ser usado

El siguiente paso consta en ejecutar la aplicacion de Django de la siguiente forma

```bash
cd CRUDPacient/utils
cd ..
python manage.py runserver
```

Este comando ejecutara una respuesta de este tipo, si tienes la misma significa que ya puedes navegar:

```bash
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
May 14, 2024 - 09:41:27
Django version 4.1.12, using settings 'CRUDPacient.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

Para ser mas claros, si todo salio bien justo ahora tendras un servidor local donde podras probar el funcionamiento de esta app encargada de las operaciones CRUD de una base de datos de pacientes de tipo relacional, con datos gubernamentales cargados y relacionados al modelo principal... Para hacer uso de las funcionalidades puedes

- [Crear](http://127.0.0.1:8000/crear/)
- [Actualizar](http://127.0.0.1:8000/actualizar/)
- [Observar](http://127.0.0.1:8000/mostrar/)
- [Eliminar](http://127.0.0.1:8000/eliminar/)

pacientes a tu gusto. Recuerda seguir todos los pasos o contactarnos en caso de alguna duda. Y no olvides que apretando CTRL + C puedes detener el servidor de Django en tiempo real. (Si tienes problemas puedes reiniciar la ejecución del servidor y volverlo a iniciar)

**Nota:** Si ya tenias tu motor de bases de datos MySQL, y tienes creado otro usuario y contraseña que te gustaria usar puedes modificar el codigo en tu version local, debes dirigirte a los archivos marcados con * y modificar las variables a tu gusto.

**Nota:** En la carpeta pacients/migrations/initial_migration podras encontrar toda la informacion y scripts usados para crear la base de datos y cargar de informacion. Y en pacients/models encontraras todas las clases que manipulan dicha estructura. :)

```bash
C:.
│   db.sqlite3
│   manage.py
│
├───CRUDPacient
│   │   asgi.py
│   │   settings.py
│   │   urls.py
│   │   wsgi.py
│   │   __init__.py
│   │
│   └───__pycache__
│           settings.cpython-312.pyc
│           urls.cpython-312.pyc
│           wsgi.cpython-312.pyc
│           __init__.cpython-312.pyc
│
├───pacients
│   │   admin.py
│   │   apps.py
│   │   Connection.py*
│   │   models.py
│   │   tests.py
│   │   urls.py
│   │   views.py
│   │   __init__.py
│   │
│   ├───migrations
│   │   │   __init__.py
│   │   │
│   │   └───initial_migration
│   │       │   CityInfoLoader.py
│   │       │   Ciudades.xlsx
│   │       │   Connection.py*
│   │       │   DataBaseCreator.py*
│   │       │   DiagnosticInfoLoader.py
│   │       │   Diagnostico.xlsx
│   │       │   NationsInfoLoader.py
│   │       │   OccuptationInfoLoader.py
│   │       │   Ocupaciones.xlsx
│   │       │   paises.xlsx
│   │       │
│   │       └───__pycache__
│   │               Connection.cpython-312.pyc
│   │
│   ├───templates
│   │       create.html
│   │       delete.html
│   │       layout.html
│   │       show.html
│   │       update.html
│   │
│   └───__pycache__
│           Connection.cpython-312.pyc
│           models.cpython-312.pyc
│           urls.cpython-312.pyc
│           views.cpython-312.pyc
│           __init__.cpython-312.pyc
│
├───utils
│       creator.py
│       __init__.py
│
└───__pycache__
        Connection.cpython-312.pyc
```
