# Generated by Django 3.2.15 on 2022-10-10 20:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Can',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=250, verbose_name='Nombre Can')),
                ('sexo', models.CharField(max_length=100, verbose_name='Sexo')),
                ('fecha_nacimiento', models.DateField(blank=True, verbose_name='Fecha de Nacimiento')),
                ('color', models.CharField(max_length=100, verbose_name='Color')),
                ('personalidad', models.TextField(blank=True, verbose_name='Personalidad')),
                ('altura', models.CharField(max_length=250, verbose_name='Tamaño')),
                ('foto', models.ImageField(default=None, upload_to='dogs_image', verbose_name='Foto del can')),
                ('adoptado', models.BooleanField(default=False, verbose_name='Estado de adopción')),
                ('esterilizado', models.BooleanField(default=False, verbose_name='Estado de esterilización')),
            ],
        ),
        migrations.CreateModel(
            name='Esterilizacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('n_tattoo', models.CharField(max_length=50, verbose_name='Numero de tatuaje')),
                ('fecha', models.DateField(verbose_name='Fecha de esterilización')),
            ],
        ),
        migrations.CreateModel(
            name='Raza',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=250, verbose_name='Nombre de Raza')),
            ],
        ),
        migrations.CreateModel(
            name='Reunion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(verbose_name='Fecha de reunión')),
                ('motivo', models.CharField(max_length=250, verbose_name='Motivo de la reunión')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario_Adoptivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_max', models.PositiveIntegerField(default=0, verbose_name='Cantidad de canes adoptados')),
            ],
        ),
        migrations.CreateModel(
            name='Vacuna',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=250, verbose_name='Vacuna')),
                ('caracteristicas', models.CharField(max_length=250, verbose_name='características')),
            ],
        ),
        migrations.CreateModel(
            name='Voluntarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Nombre')),
                ('last_name', models.CharField(max_length=250, verbose_name='Apellidos')),
                ('ci', models.PositiveIntegerField(verbose_name='Carnet de identidad')),
                ('user_charge', models.CharField(max_length=100, verbose_name='Cargo del voluntario')),
                ('birth_date', models.DateField(verbose_name='Fecha de Nacimiento')),
                ('authorization', models.BooleanField(default=False, verbose_name='Autorización')),
            ],
        ),
        migrations.CreateModel(
            name='Vacunas_Can',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(verbose_name='Fecha de vacunación')),
                ('can', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Adopciones.can')),
                ('vacuna', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Adopciones.vacuna')),
            ],
        ),
    ]
