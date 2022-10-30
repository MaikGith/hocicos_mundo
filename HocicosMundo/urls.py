from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from AppWeb.Inicio.views import LoginFormView, logoutUser
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('', include('AppWeb.Inicio.urls')),
    re_path('adopciones/', include('AppWeb.Modulos.Adopciones.urls')),
    re_path('usuarios/', include('AppWeb.Modulos.Usuarios.urls')),
    re_path('perdidos/', include('AppWeb.Modulos.Perdidos.urls')),
    re_path('donaciones/', include('AppWeb.Modulos.Donaciones.urls')),
    re_path('accounts/login/', LoginFormView.as_view(), name='login'),
    re_path('logout/', login_required(logoutUser), name='logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
