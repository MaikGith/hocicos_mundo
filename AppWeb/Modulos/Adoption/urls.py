from django.urls import path
from .views import *

urlpatterns = [
    path('listar/dog/', AdminListarDog.as_view(), name='vista_listar_dog'),
    path('registrar/dog/', AdminRegistroDog.as_view(), name='vista_registrar_dog'),
    path('listar/race/', AdminListarRace.as_view(), name='vista_listar_race'),
    path('registrar/race/', AdminRegistroRace.as_view(), name='vista_registrar_race'),
]
