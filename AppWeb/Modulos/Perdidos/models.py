from django.db import models
from AppWeb.Modulos.Adopciones.models import Can


class Perdido(models.Model):
    can_perdido = models.OneToOneField(Can, null=True, on_delete=models.SET_NULL)
    fecha = models.DateField('Fecha en que se perdió')
    comentario = models.TextField('Comentario')
