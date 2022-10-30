from django.urls import path
from .views import *

urlpatterns = [
    path('listar/', AdminListarPerdidos.as_view(), name='vista_listar_perdidos'),
    path('registrar/', AdminRegistrarPerdido.as_view(), name='vista_registrar_perdidos'),
    path('encontrado/<int:pk>/', AdminEncontrado.as_view(), name='vista_encontrado_perdidos'),
]
