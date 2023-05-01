from django.db import models
from AppWeb.Modulos.Adopciones.models import Can


class Perdido(models.Model):
    can_perdido = models.OneToOneField(Can, default=None, on_delete=models.CASCADE)
    fecha = models.DateField('Fecha en que se perdió')
    comentario = models.TextField('Comentario')
