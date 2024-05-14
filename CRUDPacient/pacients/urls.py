from django.urls import path
from . import views

urlpatterns = [
    path('',views.create_patient,name="crear_home"),
    path('crear/',views.create_patient,name="crear"),
    path('mostrar/',views.show_patient,name="mostrar"),
    path('eliminar/',views.delete_patient,name="eliminar"),
    path('actualizar/',views.update_patient,name="actualizar")
]   