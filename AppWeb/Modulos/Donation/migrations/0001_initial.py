# Generated by Django 3.2.15 on 2022-08-31 17:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Adoption', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Fecha de donación')),
                ('monto', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Monto de donación')),
                ('dog', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Adoption.dog')),
                ('user_sponsor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]