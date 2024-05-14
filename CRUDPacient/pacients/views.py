from django.shortcuts import render,redirect
from .models import Patient,OccupationDAO,NationalityDAO,CityDAO,DiagnosisDAO,PatientDAO,DonationPresumptionDocumentDAO,LivingWillDocumentDAO,DonationPresumptionDocument,LivingWillDocument
from django.contrib import messages
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

                print(documento_voluntad)

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
