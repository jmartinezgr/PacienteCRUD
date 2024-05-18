from django.shortcuts import render,redirect
from .models import Patient,OccupationDAO,NationalityDAO,CityDAO,DiagnosisDAO,PatientDAO,DonationPresumptionDocumentDAO,LivingWillDocumentDAO,DonationPresumptionDocument,LivingWillDocument
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
# Create your views here.

def create_patient(request):
    if request.method == 'POST':
        id_documento = request.POST.get('id_documento')
        tipo_documento = request.POST.get('tipo_documento')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        hora_nacimiento = request.POST.get('hora_nacimiento')
        telefono = request.POST.get('telefono')
        email = request.POST.get('email')
        direccion = request.POST.get('direccion')
        telefono_contacto = request.POST.get('telefono_contacto')
        ocupacion_id = request.POST.get('ocupacion_id')
        nacionalidad_id = request.POST.get('nacionalidad_id')
        ciudad_id = request.POST.get('ciudad_id')
        diagnostico_id = request.POST.get('diagnostico_id')
        documento_voluntad = request.POST.get('documento')
        tipo_ciudad = request.POST.get('ciudad_id_documento')
        texto_adicional = request.POST.get('texto_adicional')

        print(hora_nacimiento)
        print(fecha_nacimiento)

        ocupacion = ocupacion_id
        nacionalidad = nacionalidad_id
        ciudad = ciudad_id
        diagnostico = diagnostico_id

        patient = PatientDAO.select_one(id_documento)

        try:
            if patient is None:
                paciente = Patient(
                    id_documento,
                    tipo_documento,
                    nombre,
                    apellido,
                    fecha_nacimiento,
                    hora_nacimiento,
                    telefono,
                    email,
                    direccion,
                    telefono_contacto,
                    ocupacion,
                    nacionalidad,
                    ciudad,
                    diagnostico
                )
                PatientDAO.insert(patient=paciente)

                if documento_voluntad == "Oposicion":
                    documento = DonationPresumptionDocument(
                        id_documento,
                        texto_adicional,
                        tipo_ciudad
                    )

                    DonationPresumptionDocumentDAO.insert(documento)
                elif documento_voluntad == "Aceptacion":
                    documento = LivingWillDocument(
                        id_documento,
                        texto_adicional,
                        tipo_ciudad  
                    )

                    LivingWillDocumentDAO.insert(documento)

                messages.success(request,"Paciente Creado Exitosamente")
                return redirect('crear')
            else:
                messages.error(request,"Ocurrio un error. Ya existe un paciente con esta cedula")            
        except Exception as e:
            messages.error(request,"Ocurrio un error. No se pudo crear el paciente")
            print(e)

    ocupaciones =  OccupationDAO.select()
    nacionalidades = NationalityDAO.select()
    ciudades = CityDAO.select()
    diagnosticos = DiagnosisDAO.select()

    context = {
        'ocupaciones': ocupaciones,
        'nacionalidades': nacionalidades,
        'ciudades': ciudades,
        'diagnosticos': diagnosticos,
    }
    return render(request, 'create.html', context)

def show_patient(request):
    if request.method == 'POST':
        id_documento = request.POST.get('numero_identificacion')
        
        patient = PatientDAO.select_one(id=id_documento)
        
        if patient is None:
            messages.error(request,"No existe una persona con ese numero de identificación")
            return render(request,'show.html')
        
        
        occuptation = OccupationDAO.select_one(patient.city_id).description
        nacionalidad = NationalityDAO.select_one(patient.nationality_id).name
        ciudad = CityDAO.select_one(patient.city_id).name
        diagnostico = DiagnosisDAO.select_one(patient.diagnosis_id).description_4

        doc1 = LivingWillDocumentDAO.select_one(patient.id_document)
        doc2 = DonationPresumptionDocumentDAO.select_one(patient.id_document)

        if doc1 is not None:
            tipo_documento = "Documento de Voluntad Anticipada"
            text = doc1.content
            doc_ciudad = CityDAO.select_one(doc1.city_id).name
        elif doc2 is not None:
            tipo_documento = "Documento Presuncion Donacion"
            text = doc2.content
            doc_ciudad = CityDAO.select_one(doc2.city_id).name
        else:
            tipo_documento = "Ninguno"
            text = ""
            doc_ciudad = "Ninguna"

        if not patient is None:
            context = {
                "paciente":patient,
                "ocupacion":occuptation,
                "nacionalidad":nacionalidad,
                "ciudad":ciudad,
                "diagnostico":diagnostico,
                "tipo_documento":tipo_documento,
                "text":text,
                "doc_ciudad":doc_ciudad
            }
            return render(request,'show.html',context)
        else:
            messages.error(request,"No existe un paciente con esa informacion")

    return render(request,'show.html')

def delete_patient(request):

    if request.method == "POST":
        id_documento = request.POST.get('numero_identificacion')

        if PatientDAO.select_one(id=id_documento) is not None:
            PatientDAO.delete(id_documento)
            LivingWillDocumentDAO.delete(id_documento)
            DonationPresumptionDocumentDAO.delete(id_documento)
            messages.success(request,f"Paciente con numero de cedula {id_documento} eliminado con exito") 
        else:
            messages.error(request,"No existe un paciente con esa informacion") 

    return render(request,'delete.html')

def update_patient(request):
    if request.method == "POST":
        if 'numero_identificacion' in request.POST:
            id_documento = request.POST.get('numero_identificacion')
            patient = PatientDAO.select_one(id=id_documento)

            ocupaciones =  OccupationDAO.select()
            nacionalidades = NationalityDAO.select()
            ciudades = CityDAO.select()
            diagnosticos = DiagnosisDAO.select()

            if patient:

                #Formateamos fecha
                year = patient.birth_date.year
                month = patient.birth_date.month if patient.birth_date.month>10 else f"0{patient.birth_date.month}"
                day = patient.birth_date.day if patient.birth_date.day>10 else f"0{patient.birth_date.day}"
                patient.birth_date = f"{year}-{month}-{day}"
                delta_hora = patient.birth_time

                #Formateamos hora
                horas = delta_hora.seconds // 3600
                minutos = (delta_hora.seconds // 60) % 60
                segundos = delta_hora.seconds % 60

                # Determina si es AM o PM
                am_pm = "AM"
                if horas >= 12:
                    am_pm = "PM"
                    if horas > 12:
                        horas -= 12

                if horas < 10:
                    horas = f"0{horas}"
                else:
                    horas = str(horas)

                patient.birth_time =f"{horas}:{minutos}"
            
                doc1 = LivingWillDocumentDAO.select_one(patient.id_document)
                doc2 = DonationPresumptionDocumentDAO.select_one(patient.id_document)

                if doc1 is not None:
                    tipo_documento = "Aceptacion"
                    text = doc1.content
                    doc_ciudad = doc1.city_id
                elif doc2 is not None:
                    tipo_documento = "Oposicion"
                    text = doc2.content
                    doc_ciudad = doc2.city_id
                else:
                    tipo_documento = "Ninguno"
                    text = ""
                    doc_ciudad = ""


                context = {
                    'ocupaciones': ocupaciones,
                    'nacionalidades': nacionalidades,
                    'ciudades': ciudades,
                    'diagnosticos': diagnosticos,
                    "paciente":patient,
                    "tipo_documento":tipo_documento,
                    "text":text,
                    "doc_ciudad":doc_ciudad
                }
                return render(request,'update.html',context)
            else:
                messages.error(request,"No existe un paciente con ese numero de cedula")

        else:
            id_documento = request.POST.get('id_documento')
            tipo_documento = request.POST.get('tipo_documento')
            nombre = request.POST.get('nombre')
            apellido = request.POST.get('apellido')
            fecha_nacimiento = request.POST.get('fecha_nacimiento')
            hora_nacimiento = request.POST.get('hora_nacimiento')
            telefono = request.POST.get('telefono')
            email = request.POST.get('email')
            direccion = request.POST.get('direccion')
            telefono_contacto = request.POST.get('telefono_contacto')
            ocupacion_id = request.POST.get('ocupacion_id')
            nacionalidad_id = request.POST.get('nacionalidad_id')
            ciudad_id = request.POST.get('ciudad_id')
            diagnostico_id = request.POST.get('diagnostico_id')
            documento_voluntad = request.POST.get('documento')
            tipo_ciudad = request.POST.get('ciudad_id_documento')
            texto_adicional = request.POST.get('texto_adicional')

            ocupacion = ocupacion_id
            nacionalidad = nacionalidad_id
            ciudad = ciudad_id
            diagnostico = diagnostico_id

            try:
                paciente = Patient(
                    id_documento,
                    tipo_documento,
                    nombre,
                    apellido,
                    fecha_nacimiento,
                    hora_nacimiento,
                    telefono,
                    email,
                    direccion,
                    telefono_contacto,
                    ocupacion,
                    nacionalidad,
                    ciudad,
                    diagnostico
                )
                PatientDAO.update(paciente)

                if documento_voluntad == "Oposicion":
                    documento = DonationPresumptionDocument(
                        id_documento,
                        texto_adicional,
                        tipo_ciudad
                    )

                    DonationPresumptionDocumentDAO.insert(documento) if DonationPresumptionDocumentDAO.select_one(id_documento) is None else DonationPresumptionDocumentDAO.update(documento)
                elif documento_voluntad == "Aceptacion":
                    documento = LivingWillDocument(
                        id_documento,
                        texto_adicional,
                        tipo_ciudad  
                    )

                    LivingWillDocumentDAO.insert(documento) if LivingWillDocumentDAO.select_one(id_documento) is None else LivingWillDocumentDAO.update(documento)

                messages.success(request,"Paciente Actualizado Exitosamente")
                return render(request,'update.html')         
            except Exception as e:
                messages.error(request,"Ocurrio un error. No se pudo actualizar el paciente")
                print(e)

    return render(request,'update.html')