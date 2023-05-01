from django.db import models
from AppWeb.Modulos.Usuarios.models import User
from ckeditor.fields import RichTextField


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
    comentario = RichTextField(null=True, blank=True)
    estado = models.BooleanField(default=True)
    fecha = models.DateTimeField('Fecha de publicación', auto_now_add=True)
    usuario_creador = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.nombre_noticia
