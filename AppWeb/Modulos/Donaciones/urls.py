from django.urls import path
from .views import *

urlpatterns = [
    path('', VistaDonaciones.as_view(), name='vista_donaciones'),
    path('donar/', VistaDonar.as_view(), name='vista_donar'),
]
