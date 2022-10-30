from django.db import models
from AppWeb.Modulos.Usuarios.models import User


# Create your models here.

class Inicio(models.Model):
    nombre = models.CharField('Nombre de la imagen', max_length=250)
    imagen = models.ImageField('Imagen', upload_to="Inicio")


class Registros_usuarios(models.Model):
    tipo_movimiento = models.CharField('Acción que realizo', max_length=250)
    descripcion = models.CharField('Detalle del movimiento', max_length=250)
    usuario = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)


class Blog(models.Model):
    nombre_noticia = models.CharField('Nombre de la noticia', max_length=250)
    imagen = models.ImageField('Imagen', upload_to="Imagines_blog")
    comentario = models.TextField('Comentario', max_length=1000)
    fecha = models.DateField('Fecha de publicación', max_length=250)
    usuario_creador = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

