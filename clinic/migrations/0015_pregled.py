# Generated by Django 3.0.5 on 2020-05-08 08:51

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Model_Podataka', '0014_auto_20200502_1518'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pregled',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('klinika', models.CharField(default=None, max_length=500)),
                ('zakazan', models.CharField(default=None, max_length=500)),
                ('lekar', models.CharField(default=None, max_length=500)),
                ('sala', models.CharField(default=None, max_length=500)),
                ('tip_pregleda', models.CharField(default=None, max_length=500)),
                ('vreme', models.DateTimeField(default=None, max_length=500)),
                ('karton_pacijenta', models.CharField(default=None, max_length=500)),
                ('sifra_bolesti', models.CharField(default=None, max_length=500)),
                ('diagnoza', models.CharField(default=None, max_length=500)),
                ('lekovi', models.CharField(default=None, max_length=500)),
            ],
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]