from django.urls import path
from . import views

urlpatterns = [
    path('crear',views.create_patient,name="crear"),
]