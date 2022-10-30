from django.db import models
from AppWeb.Modulos.Usuarios.models import User


class Usuario_Adoptivo(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    cantidad_max = models.PositiveIntegerField('Cantidad de canes adoptados', default=0)


class Reunion(models.Model):
    usuario_adoptivo = models.ForeignKey(Usuario_Adoptivo, on_delete=models.CASCADE)
    fecha = models.DateField('Fecha de reunión')
    motivo = models.CharField('Motivo de la reunión', max_length=250)


class Raza(models.Model):
    nombre = models.CharField('Nombre de Raza', max_length=250)


class Vacuna(models.Model):
    nombre = models.CharField('Vacuna', max_length=250)
    caracteristicas = models.CharField('características', max_length=250)


class Can(models.Model):
    nombre = models.CharField('Nombre Can', unique=True, max_length=250)
    sexo = models.CharField('Sexo', max_length=100)
    fecha_nacimiento = models.DateField('Fecha de Nacimiento', blank=True)
    color = models.CharField('Color', max_length=100)
    personalidad = models.TextField('Personalidad', blank=True)
    altura = models.CharField('Tamaño', max_length=250)
    foto = models.ImageField('Foto del can', upload_to="dogs_image", default=None)
    adoptado = models.BooleanField('Estado de adopción', default=False)
    fecha_adopcion = models.DateField('Fecha de adopción', default=None, null=True, blank=True)
    esterilizado = models.BooleanField('Estado de esterilización', default=False)
    estado = models.BooleanField('Estado de encontrado', default=True)
    caso_independiente = models.BooleanField('Caso independiente', default=False)
    id_raza = models.ForeignKey(Raza, null=True, on_delete=models.SET_NULL)
    id_usuario_adoptivo = models.ForeignKey(Usuario_Adoptivo, default=None, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Can'
        verbose_name_plural = 'Canes'

    def __str__(self):
        return self.nombre


class Vacunas_Can(models.Model):
    vacuna = models.ForeignKey(Vacuna, null=True, on_delete=models.SET_NULL)
    can = models.ForeignKey(Can, on_delete=models.CASCADE)
    fecha = models.DateField('Fecha de vacunación')


class Esterilizacion(models.Model):
    n_tattoo = models.CharField('Numero de tatuaje', max_length=50)
    fecha = models.DateField('Fecha de esterilización')
    cam = models.OneToOneField(Can, on_delete=models.CASCADE)


class Voluntarios(models.Model):
    nombres = models.CharField('Nombre', max_length=250)
    apellidos = models.CharField('Apellidos', max_length=250)
    ci = models.CharField('Carnet de identidad', max_length=50)
    cargo = models.CharField('Cargo del voluntario', max_length=100)
    fecha_nacimiento = models.DateField('Fecha de Nacimiento')
    autorizacion = models.BooleanField('Autorización', default=False)
