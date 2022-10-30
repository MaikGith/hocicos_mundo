# Generated by Django 3.2.15 on 2022-10-10 20:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Donaciones', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='donador',
            name='usuario_donador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]