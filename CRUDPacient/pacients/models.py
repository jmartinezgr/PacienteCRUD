from .Connection import Connection
from django.db import models

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
    def __init__(self, id_document, document_type, first_name, last_name, birth_date, birth_time, phone, email, address, contact_phone, occupation_id, nationality_id, city_id, diagnosis_id):
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
        self.diagnosis_id = diagnosis_id

class Diagnosis:
    def __init__(self, id_diagnosis, code_3, description_3, code_4, description_4):
        self.id_diagnosis = id_diagnosis
        self.code_3 = code_3
        self.description_3 = description_3
        self.code_4 = code_4
        self.description_4 = description_4

#---------------------------- CLASES DAO --------------------------------------------------------------

class OccupationDAO:
    _SELECT = "SELECT * FROM ocupacion ORDER BY id_ocupacion"
    _SELECT_ONE = "SELECT * FROM ocupacion WHERE id_ocupacion = %s"
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
    def select_one(cls,id):        
        with Connection.get_cursor() as cursor:
            cursor.execute(cls._SELECT_ONE,(id,))
            register = cursor.fetchone()

            occupation = Occupation(
                register[0],
                register[1],
                register[2],
                register[3]
            ) if register else None

            return occupation 
                
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
    _SELECT_ONE = "SELECT * FROM Nacionalidad WHERE id_nacionalidad=%s"
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
    def select_one(cls, id):
        with Connection.get_cursor() as cursor:
            cursor.execute(cls._SELECT_ONE, (id,))
            register = cursor.fetchone()

            nationality = Nationality(
                register[0],
                register[1]
            ) if register else None

            return nationality
                
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
    _SELECT_ONE = "SELECT * FROM Ciudad WHERE id_ciudad=%s"
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
    def select_one(cls, id):
        with Connection.get_cursor() as cursor:
            cursor.execute(cls._SELECT_ONE, (id,))
            register = cursor.fetchone()

            city = City(
                register[0],
                register[1],
                register[2],
                register[3]
            ) if register else None

            return city
                
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
    _SELECT_ONE = "SELECT * FROM DocumentoVoluntadAnticipada WHERE id_documento=%s"
    _INSERT = "INSERT INTO DocumentoVoluntadAnticipada (id_documento,contenido, ciudad_id) VALUES (%s, %s,%s)"
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
    def select_one(cls, id):
        with Connection.get_cursor() as cursor:
            cursor.execute(cls._SELECT_ONE, (id,))
            register = cursor.fetchone()

            document = LivingWillDocument(
                register[0],
                register[1],
                register[2]
            ) if register else None

            return document
                
    @classmethod
    def insert(cls, document):
        with Connection.get_cursor() as cursor:
            try:
                cursor.execute(cls._INSERT, (document.id_document,document.content, document.city_id))
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
    _SELECT_ONE = "SELECT * FROM DocumentoPresuncionDonacion WHERE id_documento_contenido=%s"
    _INSERT = "INSERT INTO DocumentoPresuncionDonacion (id_documento_contenido,contenido, ciudad_id) VALUES (%s, %s,%s)"
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
    def select_one(cls, id):
        with Connection.get_cursor() as cursor:
            cursor.execute(cls._SELECT_ONE, (id,))
            register = cursor.fetchone()

            document = DonationPresumptionDocument(
                register[0],
                register[1],
                register[2]
            ) if register else None

            return document
                
    @classmethod
    def insert(cls, document):
        with Connection.get_cursor() as cursor:
            try:
                cursor.execute(cls._INSERT, (document.id_document_content,document.content, document.city_id))
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

class DiagnosisDAO:
    _SELECT = "SELECT * FROM Diagnostico"
    _SELECT_ONE = "SELECT * FROM Diagnostico WHERE id_diagnostico=%s"
    _INSERT = "INSERT INTO Diagnostico (cod_3, desc_3, cod_4, desc_4) VALUES (%s, %s, %s, %s)"
    _UPDATE = "UPDATE Diagnostico SET cod_3=%s, desc_3=%s, cod_4=%s, desc_4=%s WHERE id_diagnostico=%s"
    _DELETE = "DELETE FROM Diagnostico WHERE id_diagnostico=%s"

    @classmethod
    def select(cls):
        with Connection.get_cursor() as cursor:
            cursor.execute(cls._SELECT)
            registers = cursor.fetchall()

            diagnoses = []

            for register in registers:
                diagnoses.append(
                    Diagnosis(
                        register[0],
                        register[1],
                        register[2],
                        register[3],
                        register[4]
                    )
                )

            return diagnoses
        
    @classmethod
    def select_one(cls, id):
        with Connection.get_cursor() as cursor:
            cursor.execute(cls._SELECT_ONE, (id,))
            register = cursor.fetchone()

            diagnosis = Diagnosis(
                register[0],
                register[1],
                register[2],
                register[3],
                register[4]
            ) if register else None

            return diagnosis
                
    @classmethod
    def insert(cls, diagnosis):
        with Connection.get_cursor() as cursor:
            try:
                cursor.execute(cls._INSERT, (diagnosis.code_3, diagnosis.description_3, diagnosis.code_4, diagnosis.description_4))
                Connection.get_connection().commit()
            except Exception as e:
                print(f"Error creating diagnosis: {e}")

    @classmethod
    def update(cls, diagnosis):
        with Connection.get_cursor() as cursor:
            try:
                cursor.execute(cls._UPDATE, (diagnosis.code_3, diagnosis.description_3, diagnosis.code_4, diagnosis.description_4, diagnosis.id_diagnosis))
                Connection.get_connection().commit()
            except Exception as e:
                print(f"Error updating diagnosis with id {diagnosis.id_diagnosis}: {e}")

    @classmethod
    def delete(cls, id_diagnosis):
        with Connection.get_cursor() as cursor:
            try:
                cursor.execute(cls._DELETE, (id_diagnosis,))
                Connection.get_connection().commit()
            except Exception as e:
                print(f"Error deleting diagnosis with id {id_diagnosis}: {e}")

class PatientDAO:
    _SELECT = "SELECT * FROM Paciente"
    _SELECT_ONE = "SELECT * FROM Paciente WHERE id_documento=%s"
    _INSERT = """
        INSERT INTO Paciente (id_documento, tipo_documento, nombre, apellido, fecha_nacimiento, hora_nacimiento, telefono, email, direccion, telefono_contacto, ocupacion_id, nacionalidad_id, ciudad_id, diagnostico_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    _UPDATE = """
        UPDATE Paciente SET tipo_documento=%s, nombre=%s, apellido=%s, fecha_nacimiento=%s, hora_nacimiento=%s, telefono=%s, email=%s, direccion=%s, telefono_contacto=%s, ocupacion_id=%s, nacionalidad_id=%s, ciudad_id=%s, diagnostico_id=%s
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
                        register[12],
                        register[13]  # Add diagnosis_id to Patient instantiation
                    )
                )

            return patients
        
    @classmethod
    def select_one(cls, id):
        with Connection.get_cursor() as cursor:
            cursor.execute(cls._SELECT_ONE, (id,))
            register = cursor.fetchone()

            patient = Patient(
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
                register[12],
                register[13]  
            ) if register else None

            return patient
                
    @classmethod
    def insert(cls, patient):
        with Connection.get_cursor() as cursor:
            try:
                cursor.execute(cls._INSERT, (
                    patient.id_document, patient.document_type, patient.first_name, patient.last_name,
                    patient.birth_date, patient.birth_time, patient.phone, patient.email,
                    patient.address, patient.contact_phone, patient.occupation_id,
                    patient.nationality_id, patient.city_id, patient.diagnosis_id
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
                    patient.diagnosis_id, patient.id_document
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
    # Obtener el registro con ID 1 de cada tabla y mostrar la información
    
    # Obtener la ocupación con ID 1
    occupation = OccupationDAO.select_one(1)
    if occupation:
        print("Occupation with ID 1:")
        print(f"ID: {occupation.id_occupation}, Code: {occupation.code}, Description: {occupation.description}, Father Code: {occupation.father_code}")
    else:
        print("Occupation with ID 1 not found.")

    # Obtener la nacionalidad con ID 1
    nationality = NationalityDAO.select_one(1)
    if nationality:
        print("\nNationality with ID 1:")
        print(f"ID: {nationality.id_nationality}, Name: {nationality.name}")
    else:
        print("Nationality with ID 1 not found.")

    # Obtener la ciudad con ID 1
    city = CityDAO.select_one(1)
    if city:
        print("\nCity with ID 1:")
        print(f"ID: {city.id_city}, Name: {city.name}, Dane Code: {city.dane_code}, Type: {city.type}")
    else:
        print("City with ID 1 not found.")

    # Obtener el documento de voluntad anticipada con ID 1
    living_will_document = LivingWillDocumentDAO.select_one(1)
    if living_will_document:
        print("\nLiving Will Document with ID 1:")
        print(f"ID: {living_will_document.id_document}, Content: {living_will_document.content}, City ID: {living_will_document.city_id}")
    else:
        print("Living Will Document with ID 1 not found.")

    # Obtener el documento de presunción de donación con ID 1
    donation_presumption_document = DonationPresumptionDocumentDAO.select_one(1)
    if donation_presumption_document:
        print("\nDonation Presumption Document with ID 1:")
        print(f"ID: {donation_presumption_document.id_document_content}, Content: {donation_presumption_document.content}, City ID: {donation_presumption_document.city_id}")
    else:
        print("Donation Presumption Document with ID 1 not found.")

    # Obtener el diagnóstico con ID 1
    diagnosis = DiagnosisDAO.select_one(1)
    if diagnosis:
        print("\nDiagnosis with ID 1:")
        print(f"ID: {diagnosis.id_diagnosis}, Code 3: {diagnosis.code_3}, Description 3: {diagnosis.description_3}, Code 4: {diagnosis.code_4}, Description 4: {diagnosis.description_4}")
    else:
        print("Diagnosis with ID 1 not found.")

    # Obtener el paciente con ID 1
    patient = PatientDAO.select_one(123456789)
    if patient:
        print("\nPatient with ID 123456789:")
        print(f"ID: {patient.id_document}, Document Type: {patient.document_type}, First Name: {patient.first_name}, Last Name: {patient.last_name}, Birth Date: {patient.birth_date}, Birth Time: {patient.birth_time}, Phone: {patient.phone}, Email: {patient.email}, Address: {patient.address}, Contact Phone: {patient.contact_phone}, Occupation ID: {patient.occupation_id}, Nationality ID: {patient.nationality_id}, City ID: {patient.city_id}, Diagnosis ID: {patient.diagnosis_id}")
    else:
        print("Patient with ID 1 not found.")

if __name__ == "__main__":
    main()
