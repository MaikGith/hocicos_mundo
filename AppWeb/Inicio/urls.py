from django.urls import path
from .views import *

urlpatterns = [
    path('', Index.as_view(), name='Index'),
    path('adopciones/', PaginaAdopciones.as_view(), name='pagina_adopciones'),
    path('administrador/', Administration.as_view(), name='Administrador'),
]
