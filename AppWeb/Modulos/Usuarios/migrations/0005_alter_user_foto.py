# Generated by Django 3.2.15 on 2022-10-28 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Usuarios', '0004_alter_user_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='foto',
            field=models.ImageField(blank=True, default='Usuarios/fondo.jpg', upload_to='Usuarios', verbose_name='Foto del usuario'),
        ),
    ]
