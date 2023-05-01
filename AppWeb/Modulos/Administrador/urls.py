from django.urls import path
from .views import *

urlpatterns = [
    path('', AdminListarBlog.as_view(), name='vista_listar_blog'),
    path('registrar/', AdminRegistrarBlog.as_view(), name='vista_registrar_blog'),
    path('estado/<int:pk>/', AdminEstadoBlog.as_view(), name='vista_estado_blog'),
    path('editar/<int:pk>/', AdminEditarBlog.as_view(), name='vista_editar_blog'),
    path('eliminar/<int:pk>/', AdminEliminarBlog.as_view(), name='vista_eliminar_blog'),
    path('imagenes/listar/', AdminListarImagenes.as_view(), name='vista_listar_imagenes'),
    path('imagenes/registrar/', AdminRegistrarImagen.as_view(), name='vista_registrar_imagenes'),
    path('imagenes/editar/<int:pk>/', AdminEditarImagen.as_view(), name='vista_editar_imagenes'),
    path('imagenes/eliminar/<int:pk>/', AdminEliminarImagen.as_view(), name='vista_eliminar_imagenes'),
    path('movimientos/listar/', AdminListarMovimientos.as_view(), name='vista_listar_movimientos'),
]
