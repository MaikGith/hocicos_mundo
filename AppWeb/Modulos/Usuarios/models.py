from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import UserManager


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('Nombre de usuario', max_length=250, blank=True)
    email = models.EmailField('Email', unique=True)
    nombres = models.CharField('Nombres', max_length=250, blank=True)
    apellidos = models.CharField('Apellidos', max_length=250, blank=True)
    celular = models.PositiveIntegerField('Numero telefónico', null=True)
    foto = models.ImageField('Foto del usuario', upload_to="Usuarios", default='Usuarios/fondo.jpg', blank=True)
    ci = models.CharField('Carnet de identidad', max_length=20, blank=True)
    direccion = models.CharField('Dirección', max_length=254, blank=True)
    is_padrino = models.BooleanField('Padrino', default=False)
    is_staff = models.BooleanField('Usuario staff', default=False)
    is_superuser = models.BooleanField('Super usuario', default=False)
    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username', ]
    objects = UserManager()

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return self.nombres + ' ' + self.apellidos
