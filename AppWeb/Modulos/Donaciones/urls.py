from django.urls import path
from .views import *

urlpatterns = [
    path('', VistaDonaciones.as_view(), name='vista'),
    path('donar/', VistaDonar.as_view(), name='vista_donar'),
    path('donacion/<int:pk>/', SolicitarPadrinaje.as_view(), name='vista_solicitar_padrinaje'),
    path('donaciones/', Donaciones.as_view(), name='vista_donaciones'),
    path('registrar/<int:pk>', RegistrarDonacion.as_view(), name='vista_registrar_donacion'),
    path('historial/<int:pk>', HistorialDonaciones.as_view(), name='vista_historial_donacion'),
    path('editar/<int:pk>', EditarDonacion.as_view(), name='vista_editar_donacion'),
    path('eliminar/<int:pk>/', EliminarDonacion.as_view(), name='vista_eliminar_donacion'),
]
