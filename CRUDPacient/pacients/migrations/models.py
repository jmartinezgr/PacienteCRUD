from CRUDPacient.pacients.migrations.initial_migration.Connection import Connection

class Occupation:
    def __init__(self, id_occupation, code, description, father_code) -> None:
        self.id_occupation = id_occupation
        self.code = code
        self.description = description
        self.father_code = father_code

class Nationality:
    def __init__(self, id_nationality, name):
        self.id_nationality = id_nationality
        self.name = name

class City:
    def __init__(self, id_city, name, dane_code, type):
        self.id_city = id_city
        self.name = name
        self.dane_code = dane_code
        self.type = type

class LivingWillDocument:
    def __init__(self, id_document, content, city_id):
        self.id_document = id_document
        self.content = content
        self.city_id = city_id

class DonationPresumptionDocument:
    def __init__(self, id_document_content, content, city_id):
        self.id_document_content = id_document_content
        self.content = content
        self.city_id = city_id

class Patient:
    def __init__(self, id_document, document_type, first_name, last_name, birth_date, birth_time, phone, email, address, contact_phone, occupation_id, nationality_id, city_id):
        self.id_document = id_document
        self.document_type = document_type
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.birth_time = birth_time
        self.phone = phone
        self.email = email
        self.address = address
        self.contact_phone = contact_phone
        self.occupation_id = occupation_id
        self.nationality_id = nationality_id
        self.city_id = city_id

#---------------------------- CLASES DAO --------------------------------------------------------------

class OccupationDAO:
    _SELECT = "SELECT * FROM ocupacion ORDER BY id_ocupacion"
    _INSERT = "INSERT INTO ocupacion (codigo, descripcion, codigo_padre) VALUES (%s, %s, %s)"
    _UPDATE = "UPDATE ocupacion SET codigo=%s, descripcion=%s, codigo_padre=%s WHERE id_ocupacion=%s"
    _DELETE = "DELETE FROM ocupacion WHERE id_ocupacion=%s"

    @classmethod
    def select(cls):
        with Connection.get_cursor() as cursor:
            cursor.execute(cls._SELECT)
            registers = cursor.fetchall()
            occupations = []

            for register in registers:
                occupations.append(
                    Occupation(
                        register[0],
                        register[1],
                        register[2],
                        register[3]
                    )
                )

            return occupations
                
    @classmethod
    def insert(cls, code=None, description=None, father_code=None, occupation=None):
        if occupation:
            code = occupation.code
            description = occupation.description
            father_code = occupation.father_code

        connection = Connection.get_connection()
        cursor = Connection.get_cursor()
        try:
            cursor.execute(cls._INSERT, (code, description, father_code))
            connection.commit()  
        except Exception as e:
            connection.rollback()  
            print(f"Error creating occupation: {e}")
        finally:
            cursor.close()  
            
    @classmethod
    def update(cls, id=None, code=None, description=None, father_code=None, occupation=None):
        if occupation:
            id = occupation.id_occupation
            code = occupation.code
            description = occupation.description
            father_code = occupation.father_code

        connection = Connection.get_connection()
        cursor = Connection.get_cursor()
        try:
            cursor.execute(cls._UPDATE, (code, description, father_code, id))
            connection.commit()  
        except Exception as e:
            connection.rollback()  
            print(f"Error updating occupation with id {id}: {e}")
        finally:
            cursor.close()  
                
    @classmethod
    def delete(cls, id=None, occupation=None):
        if occupation:
            id = occupation.id_occupation

        connection = Connection.get_connection()
        cursor = Connection.get_cursor()
        try:
            cursor.execute(cls._DELETE, (id,))
            connection.commit()  
        except Exception as e:
            connection.rollback()  
            print(f"Error deleting occupation with id {id}: {e}")
        finally:
            cursor.close() 

class NationalityDAO:
    _SELECT = "SELECT * FROM Nacionalidad"
    _INSERT = "INSERT INTO Nacionalidad (id_nacionalidad,nombre) VALUES (%s,%s)"
    _UPDATE = "UPDATE Nacionalidad SET nombre=%s WHERE id_nacionalidad=%s"
    _DELETE = "DELETE FROM Nacionalidad WHERE id_nacionalidad=%s"

    @classmethod
    def select(cls):
        with Connection.get_cursor() as cursor:
            cursor.execute(cls._SELECT)
            registers = cursor.fetchall()
            
            nationalities = []
            
            for register in registers:
                nationalities.append(
                    Nationality(
                        register[0],
                        register[1]
                    )
                )

            return nationalities
                
    @classmethod
    def insert(cls, nationality):
        with Connection.get_cursor() as cursor:
            try:
                cursor.execute(cls._INSERT, (nationality.name,))
                Connection.get_connection().commit()
            except Exception as e:
                print(f"Error creating nationality: {e}")

    @classmethod
    def update(cls, nationality):
        with Connection.get_cursor() as cursor:
            try:
                cursor.execute(cls._UPDATE, (nationality.name, nationality.id_nationality))
                Connection.get_connection().commit()
            except Exception as e:
                print(f"Error updating nationality with id {nationality.id_nationality}: {e}")

    @classmethod
    def delete(cls, id_nationality):
        with Connection.get_cursor() as cursor:
            try:
                cursor.execute(cls._DELETE, (id_nationality,))
                Connection.get_connection().commit()
            except Exception as e:
                print(f"Error deleting nationality with id {id_nationality}: {e}")

class CityDAO:
    _SELECT = "SELECT * FROM Ciudad"
    _INSERT = "INSERT INTO Ciudad (nombre, codigo_dane, tipo) VALUES (%s, %s, %s)"
    _UPDATE = "UPDATE Ciudad SET nombre=%s, codigo_dane=%s, tipo=%s WHERE id_ciudad=%s"
    _DELETE = "DELETE FROM Ciudad WHERE id_ciudad=%s"

    @classmethod
    def select(cls):
        with Connection.get_cursor() as cursor:
            cursor.execute(cls._SELECT)
            registers = cursor.fetchall()

            cities = []

            for register in registers:
                cities.append(
                    City(
                        register[0],
                        register[1],
                        register[2],
                        register[3]
                    )
                )

            return cities
                
    @classmethod
    def insert(cls, city):
        with Connection.get_cursor() as cursor:
            try:
                cursor.execute(cls._INSERT, (city.name, city.dane_code, city.type))
                Connection.get_connection().commit()
            except Exception as e:
                print(f"Error creating city: {e}")

    @classmethod
    def update(cls, city):
        with Connection.get_cursor() as cursor:
            try:
                cursor.execute(cls._UPDATE, (city.name, city.dane_code, city.type, city.id_city))
                Connection.get_connection().commit()
            except Exception as e:
                print(f"Error updating city with id {city.id_city}: {e}")

class LivingWillDocumentDAO:
    _SELECT = "SELECT * FROM DocumentoVoluntadAnticipada"
    _INSERT = "INSERT INTO DocumentoVoluntadAnticipada (contenido, ciudad_id) VALUES (%s, %s)"
    _UPDATE = "UPDATE DocumentoVoluntadAnticipada SET contenido=%s, ciudad_id=%s WHERE id_documento=%s"
    _DELETE = "DELETE FROM DocumentoVoluntadAnticipada WHERE id_documento=%s"

    @classmethod
    def select(cls):
        with Connection.get_cursor() as cursor:
            cursor.execute(cls._SELECT)
            registers = cursor.fetchall()

            documents = []

            for register in registers:
                documents.append(
                    LivingWillDocument(
                        register[0],
                        register[1],
                        register[2]
                    )
                )

            return documents
                
    @classmethod
    def insert(cls, document):
        with Connection.get_cursor() as cursor:
            try:
                cursor.execute(cls._INSERT, (document.content, document.city_id))
                Connection.get_connection().commit()
            except Exception as e:
                print(f"Error creating living will document: {e}")

    @classmethod
    def update(cls, document):
        with Connection.get_cursor() as cursor:
            try:
                cursor.execute(cls._UPDATE, (document.content, document.city_id, document.id_document))
                Connection.get_connection().commit()
            except Exception as e:
                print(f"Error updating living will document with id {document.id_document}: {e}")

    @classmethod
    def delete(cls, id_document):
        with Connection.get_cursor() as cursor:
            try:
                cursor.execute(cls._DELETE, (id_document,))
                Connection.get_connection().commit()
            except Exception as e:
                print(f"Error deleting living will document with id {id_document}: {e}")

class DonationPresumptionDocumentDAO:
    _SELECT = "SELECT * FROM DocumentoPresuncionDonacion"
    _INSERT = "INSERT INTO DocumentoPresuncionDonacion (contenido, ciudad_id) VALUES (%s, %s)"
    _UPDATE = "UPDATE DocumentoPresuncionDonacion SET contenido=%s, ciudad_id=%s WHERE id_documento_contenido=%s"
    _DELETE = "DELETE FROM DocumentoPresuncionDonacion WHERE id_documento_contenido=%s"

    @classmethod
    def select(cls):
        with Connection.get_cursor() as cursor:
            cursor.execute(cls._SELECT)
            registers = cursor.fetchall()

            documents = []

            for register in registers:
                documents.append(
                    DonationPresumptionDocument(
                        register[0],
                        register[1],
                        register[2]
                    )
                )

            return documents
                
    @classmethod
    def insert(cls, document):
        with Connection.get_cursor() as cursor:
            try:
                cursor.execute(cls._INSERT, (document.content, document.city_id))
                Connection.get_connection().commit()
            except Exception as e:
                print(f"Error creating donation presumption document: {e}")

    @classmethod
    def update(cls, document):
        with Connection.get_cursor() as cursor:
            try:
                cursor.execute(cls._UPDATE, (document.content, document.city_id, document.id_document_content))
                Connection.get_connection().commit()
            except Exception as e:
                print(f"Error updating donation presumption document with id {document.id_document_content}: {e}")

    @classmethod
    def delete(cls, id_document_content):
        with Connection.get_cursor() as cursor:
            try:
                cursor.execute(cls._DELETE, (id_document_content,))
                Connection.get_connection().commit()
            except Exception as e:
                print(f"Error deleting donation presumption document with id {id_document_content}: {e}")

class PatientDAO:
    _SELECT = "SELECT * FROM Paciente"
    _INSERT = """
        INSERT INTO Paciente (id_documento, tipo_documento, nombre, apellido, fecha_nacimiento, hora_nacimiento, telefono, email, direccion, telefono_contacto, ocupacion_id, nacionalidad_id, ciudad_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    _UPDATE = """
        UPDATE Paciente SET tipo_documento=%s, nombre=%s, apellido=%s, fecha_nacimiento=%s, hora_nacimiento=%s, telefono=%s, email=%s, direccion=%s, telefono_contacto=%s, ocupacion_id=%s, nacionalidad_id=%s, ciudad_id=%s
        WHERE id_documento=%s
    """
    _DELETE = "DELETE FROM Paciente WHERE id_documento=%s"

    @classmethod
    def select(cls):
        with Connection.get_cursor() as cursor:
            cursor.execute(cls._SELECT)
            registers = cursor.fetchall()

            patients = []

            for register in registers:
                patients.append(
                    Patient(
                        register[0],
                        register[1],
                        register[2],
                        register[3],
                        register[4],
                        register[5],
                        register[6],
                        register[7],
                        register[8],
                        register[9],
                        register[10],
                        register[11],   
                        register[12]                     
                    )
                )

            return patients
                
    @classmethod
    def insert(cls, patient):
        with Connection.get_cursor() as cursor:
            try:
                cursor.execute(cls._INSERT, (
                    patient.id_document, patient.document_type, patient.first_name, patient.last_name,
                    patient.birth_date, patient.birth_time, patient.phone, patient.email,
                    patient.address, patient.contact_phone, patient.occupation_id,
                    patient.nationality_id, patient.city_id
                ))
                Connection.get_connection().commit()
            except Exception as e:
                print(f"Error creating patient: {e}")

    @classmethod
    def update(cls, patient):
        with Connection.get_cursor() as cursor:
            try:
                cursor.execute(cls._UPDATE, (
                    patient.document_type, patient.first_name, patient.last_name, patient.birth_date,
                    patient.birth_time, patient.phone, patient.email, patient.address,
                    patient.contact_phone, patient.occupation_id, patient.nationality_id, patient.city_id,
                    patient.id_document
                ))
                Connection.get_connection().commit()
            except Exception as e:
                print(f"Error updating patient with id {patient.id_document}: {e}")

    @classmethod
    def delete(cls, id_document):
        with Connection.get_cursor() as cursor:
            try:
                cursor.execute(cls._DELETE, (id_document,))
                Connection.get_connection().commit()
            except Exception as e:
                print(f"Error deleting patient with id {id_document}: {e}")

def main():
    # Crear ejemplos de las ocupaciones, nacionalidades y ciudades
    ocupacion = Occupation(None, '001', 'Ingeniero', None)
    nacionalidad = Nationality(None, 'Colombiana')
    ciudad = City(None, 'Bogotá', '11001', 'Urbana')

    # Insertar ejemplos en la base de datos
    #OccupationDAO.insert(occupation=ocupacion)
    #NationalityDAO.insert(nationality=nacionalidad)
    #CityDAO.insert(city=ciudad)
    # Seleccionar los registros recién insertados para obtener sus IDs
    ocupaciones = OccupationDAO.select()
    nacionalidades =  NationalityDAO.select()
    ciudades = CityDAO.select()

    # Usar los IDs de los registros insertados para crear un paciente
    paciente = Patient(
        id_document = '123456789',
        document_type = 'CC',
        first_name = 'Juan',
        last_name = 'Pérez',
        birth_date = '1990-01-01',
        birth_time = '08:00',
        phone = '123456789',
        email = 'juan.perez@example.com',
        address = 'Calle Falsa 123',
        contact_phone ='987654321',
        occupation_id = ocupaciones[0].id_occupation,
        nationality_id = nacionalidades[0].id_nationality,
        city_id = 4#ciudades[0].id_city
    )

    # Insertar el paciente en la base de datos
    PatientDAO.insert(paciente)

if __name__ == "__main__":
    main()