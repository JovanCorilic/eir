# Generated by Django 3.0.5 on 2020-06-06 07:36

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Operacije',
            fields=[
                ('id', models.CharField(default=None, max_length=500, primary_key=True, serialize=False)),
                ('klinika', models.CharField(default=None, max_length=500)),
                ('pacijent', models.CharField(default=None, max_length=500)),
                ('lekari', models.CharField(default=None, max_length=500)),
                ('sala', models.CharField(default=None, max_length=500)),
                ('tip_operacije', models.CharField(default=None, max_length=500)),
                ('vreme', models.DateTimeField(default=None, max_length=500)),
                ('ocenaLekara', models.CharField(default='-1', max_length=500)),
                ('ocenaKlinike', models.FloatField(default=-1)),
            ],
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Pacijent',
            fields=[
                ('email_adresa', models.CharField(default=None, max_length=500, primary_key=True, serialize=False)),
                ('lozinka', models.CharField(default=None, max_length=500)),
                ('ime', models.CharField(default=None, max_length=500)),
                ('prezime', models.CharField(default=None, max_length=500)),
                ('adresa_prebivalista', models.CharField(default=None, max_length=500)),
                ('grad', models.CharField(default=None, max_length=500)),
                ('drzava', models.CharField(default=None, max_length=500)),
                ('broja_telefona', models.CharField(default=None, max_length=500)),
                ('jedinstveni_broj_osiguranika', models.CharField(default=None, max_length=500)),
                ('sifra_bolesti', models.CharField(default=None, max_length=500)),
                ('datum', models.CharField(default=None, max_length=500)),
                ('diagnoza', models.CharField(default=None, max_length=500)),
                ('lekovi', models.CharField(default=None, max_length=500)),
                ('dioptrija', models.CharField(default=None, max_length=500)),
                ('alergije_na_lek', models.CharField(default=None, max_length=500)),
                ('visina', models.CharField(default=None, max_length=500)),
                ('tezina', models.CharField(default=None, max_length=500)),
                ('krvna_grupa', models.CharField(default=None, max_length=500)),
                ('aktiviran', models.IntegerField(default=1)),
            ],
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Pregled',
            fields=[
                ('id', models.CharField(default=None, max_length=500, primary_key=True, serialize=False)),
                ('klinika', models.CharField(default=None, max_length=500)),
                ('zakazan', models.CharField(default=None, max_length=500)),
                ('lekar', models.CharField(default=None, max_length=500)),
                ('sala', models.CharField(default=None, max_length=500)),
                ('tip_pregleda', models.CharField(default=None, max_length=500)),
                ('vreme', models.DateTimeField(default=None, max_length=500)),
                ('sifra_bolesti', models.CharField(default=None, max_length=500)),
                ('diagnoza', models.CharField(default=None, max_length=500)),
                ('lekovi', models.CharField(default=None, max_length=500)),
                ('prihvacen', models.CharField(default='da', max_length=500)),
                ('ocenaLekara', models.FloatField(default=-1)),
                ('ocenaKlinike', models.FloatField(default=-1)),
            ],
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
