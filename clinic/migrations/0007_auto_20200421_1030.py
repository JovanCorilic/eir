# Generated by Django 3.0.5 on 2020-04-21 08:30

import django.contrib.auth.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Model_Podataka', '0006_auto_20200421_1025'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='klinika',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='sala',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
