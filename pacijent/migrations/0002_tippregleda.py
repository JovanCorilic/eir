# Generated by Django 3.0.5 on 2020-08-22 18:07

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pacijent', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipPregleda',
            fields=[
                ('id', models.CharField(default=None, max_length=500, primary_key=True, serialize=False)),
                ('ime', models.CharField(default=None, max_length=500)),
                ('cena', models.CharField(default=None, max_length=500)),
                ('trajanje', models.CharField(default=None, max_length=500)),
            ],
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
