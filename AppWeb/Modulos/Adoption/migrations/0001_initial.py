# Generated by Django 3.2.15 on 2022-08-31 17:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Dog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Nombre Can')),
                ('specie', models.CharField(max_length=100, verbose_name='Especie')),
                ('sex', models.CharField(max_length=100, verbose_name='Sexo')),
                ('birth_date', models.DateField(blank=True, verbose_name='Fecha de Nacimiento')),
                ('color', models.CharField(max_length=100, verbose_name='Color')),
                ('personality', models.TextField(blank=True, verbose_name='Personalidad')),
                ('size', models.CharField(max_length=250, verbose_name='Tamaño')),
                ('photo', models.ImageField(default=None, upload_to='dogs_image', verbose_name='Foto del can')),
                ('adopted', models.BooleanField(default=False, verbose_name='Estado de adopción')),
            ],
        ),
        migrations.CreateModel(
            name='Race',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Nombre de Raza')),
            ],
        ),
        migrations.CreateModel(
            name='Vaccine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Vacuna')),
                ('features', models.CharField(max_length=250, verbose_name='características')),
            ],
        ),
        migrations.CreateModel(
            name='Volunteers',
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
            name='Vaccines',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Fecha de vacunación')),
                ('dog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Adoption.dog')),
                ('vaccine', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Adoption.vaccine')),
            ],
        ),
        migrations.CreateModel(
            name='UserAdoptive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ci', models.CharField(max_length=20, verbose_name='Carnet de identidad')),
                ('direccion', models.CharField(max_length=254, verbose_name='Dirección')),
                ('photo', models.ImageField(default=None, upload_to='UserAdoptive_image', verbose_name='Foto del can')),
                ('cantidad_max', models.PositiveIntegerField(default=0, verbose_name='Cantidad de canes adoptados')),
                ('person_adoptive', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sterilization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('n_tattoo', models.CharField(max_length=50, verbose_name='Numero de tatuaje')),
                ('date', models.DateField(verbose_name='Fecha de esterilización')),
                ('dog', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Adoption.dog')),
            ],
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Fecha de reunión')),
                ('reason', models.CharField(max_length=250, verbose_name='Motivo de la reunión')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Adoption.useradoptive')),
            ],
        ),
        migrations.AddField(
            model_name='dog',
            name='race',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Adoption.race'),
        ),
        migrations.AddField(
            model_name='dog',
            name='user_adoptive',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Adoption.useradoptive'),
        ),
    ]