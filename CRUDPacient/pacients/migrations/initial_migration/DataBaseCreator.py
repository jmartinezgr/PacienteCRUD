import pymysql

# Conectarse al servidor MySQL
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

try:
    # Crear un cursor
    with conn.cursor() as cursor:

        # Crear la base de datos
        sql_create_db = "CREATE DATABASE IF NOT EXISTS CRUDINFO"
        cursor.execute(sql_create_db)

        # Usar la base de datos
        cursor.execute("USE CRUDINFO")

        # Crear la tabla Ocupacion
        sql_create_occupation_table = """
        CREATE TABLE IF NOT EXISTS Ocupacion (
            id_ocupacion INT AUTO_INCREMENT PRIMARY KEY,
            codigo INT,
            descripcion VARCHAR(255),
            codigo_padre INT
        )
        """
        cursor.execute(sql_create_occupation_table)

        # Crear la tabla Nacionalidad
        sql_create_nationality_table = """
        CREATE TABLE IF NOT EXISTS Nacionalidad (
            id_nacionalidad varchar(4) PRIMARY KEY,
            nombre VARCHAR(255)
        )
        """
        cursor.execute(sql_create_nationality_table)

        # Crear la tabla Ciudad
        sql_create_city_table = """
        CREATE TABLE IF NOT EXISTS Ciudad (
            id_ciudad INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(255),
            codigo_dane INT,
            tipo VARCHAR(20)
        )
        """
        cursor.execute(sql_create_city_table)

        # Crear la tabla DocumentoVoluntadAnticipada
        sql_create_voluntary_table = """
        CREATE TABLE IF NOT EXISTS DocumentoVoluntadAnticipada (
            id_documento VARCHAR(20) PRIMARY KEY,
            contenido VARCHAR(1000),
            ciudad_id INT,
            FOREIGN KEY (ciudad_id) REFERENCES Ciudad(id_ciudad)
        )
        """
        cursor.execute(sql_create_voluntary_table)

        # Crear la tabla DocumentoPresuncionDonacion
        sql_create_donation_table = """
        CREATE TABLE IF NOT EXISTS DocumentoPresuncionDonacion (
            id_documento_contenido VARCHAR(20) PRIMARY KEY,
            contenido VARCHAR(1000),
            ciudad_id INT,
            FOREIGN KEY (ciudad_id) REFERENCES Ciudad(id_ciudad)
        )
        """
        cursor.execute(sql_create_donation_table)

        sql_create_diagnostic_table = """
        CREATE TABLE IF NOT EXISTS Diagnostico(
            id_diagnostico INT AUTO_INCREMENT PRIMARY KEY,
            cod_3 VARCHAR(3),
            desc_3 VARCHAR(200),
            cod_4 VARCHAR(4),
            desc_4 VARCHAR(200)
        ) 
        """

        cursor.execute(sql_create_diagnostic_table)

        # Crear la tabla Paciente
        sql_create_patient_table = """
        CREATE TABLE IF NOT EXISTS Paciente (
            id_documento VARCHAR(20) PRIMARY KEY,
            tipo_documento VARCHAR(20),
            nombre VARCHAR(255),
            apellido VARCHAR(255),
            fecha_nacimiento DATE,
            hora_nacimiento TIME,
            telefono VARCHAR(20),
            email VARCHAR(255),
            direccion VARCHAR(255),
            telefono_contacto VARCHAR(20),
            ocupacion_id INT,
            nacionalidad_id varchar(4),
            ciudad_id INT,
            diagnostico_id INT,  -- Aquí especificamos el tipo de datos INT
            FOREIGN KEY (ocupacion_id) REFERENCES Ocupacion(id_ocupacion),
            FOREIGN KEY (nacionalidad_id) REFERENCES Nacionalidad(id_nacionalidad),
            FOREIGN KEY (ciudad_id) REFERENCES Ciudad(id_ciudad),
            FOREIGN KEY (diagnostico_id) REFERENCES Diagnostico(id_diagnostico)
        )
        """
        cursor.execute(sql_create_patient_table)

    # Confirmar la operación
    conn.commit()

finally:
    # Cerrar la conexión
    conn.close()