from django.urls import path
from .views import *

urlpatterns = [
    path('', Index.as_view(), name='Index'),
    path('adopciones/', PaginaAdopciones.as_view(), name='pagina_adopciones'),
    path('padrinaje/', PaginaPadrinaje.as_view(), name='pagina_padrinaje'),
    path('perdido/', PaginaPerdidos.as_view(), name='pagina_perdidos'),
    path('perdido/<int:pk>', InformacionPerdido.as_view(), name='informacion_perdido'),
    path('blog/', PaginaBlog.as_view(), name='pagina_blog'),
    path('blog/contenido/<int:pk>/', PaginaBlogContenido.as_view(), name='pagina_blog_contenido'),
    path('quienes_somos/', PaginaQuienesSomos.as_view(), name='pagina_quienes_somos'),
    path('administrador/', Administrador.as_view(), name='Administrador'),
]
