from django.urls import path
from .views import *

urlpatterns = [
    path('listar/', AdminListarUsuarios.as_view(), name='vista_listar_usuarios'),
    path('registrar/', AdminRegistroUsuarios.as_view(), name='vista_registrar_usuarios'),
    path('eliminar/<int:pk>/', AdminEliminarUsuario.as_view(), name='vista_eliminar_usuarios'),
    path('login/', LoginUsuarios.as_view(), name='vista_login_usuarios'),
    path('logout/', LogoutUsuarios.as_view(), name='vista_logout_usuarios'),
    path('adoptantes/listar/', AdminListarAdoptantes.as_view(), name='vista_listar_adoptantes'),
    path('adoptantes/registrar/', AdminRegistroAdoptantes.as_view(), name='vista_registrar_adoptantes'),
    path('adoptantes/editar/<int:pk>/', AdminEditarAdoptante.as_view(), name='vista_editar_adoptantes'),
    path('adoptantes/eliminar/<int:pk>/', AdminEliminarAdoptante.as_view(), name='vista_eliminar_adoptantes'),
    path('padrinos/listar/', AdminListarPadrinos.as_view(), name='vista_listar_padrinos'),
    path('padrinos/registrar/', AdminRegistroPadrinos.as_view(), name='vista_registrar_padrinos'),
    path('padrinos/editar/<int:pk>/', AdminEditarPadrino.as_view(), name='vista_editar_padrinos'),
    path('padrinos/eliminar/<int:pk>/', AdminEliminarPadrino.as_view(), name='vista_eliminar_padrino'),
    path('voluntarios/listar/', AdminListarVoluntarios.as_view(), name='vista_listar_voluntarios'),
    path('voluntarios/registrar/', AdminRegistroVoluntarios.as_view(), name='vista_registrar_voluntarios'),
    path('voluntarios/editar/<int:pk>/', AdminEditarVoluntarios.as_view(), name='vista_editar_voluntarios'),
    path('voluntarios/eliminar/<int:pk>/', AdminEliminarVoluntarios.as_view(), name='vista_eliminar_voluntarios'),
]
