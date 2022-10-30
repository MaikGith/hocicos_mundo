# Generated by Django 3.2.15 on 2022-10-10 20:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Adopciones', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Perdido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(verbose_name='Fecha en que se perdió')),
                ('encontrado', models.BooleanField(default=False, verbose_name='Estado de encontrado')),
                ('comentario', models.TextField(verbose_name='Comentario')),
                ('can_perdido', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Adopciones.can')),
            ],
        ),
    ]