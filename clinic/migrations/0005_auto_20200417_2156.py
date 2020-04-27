# Generated by Django 2.2.12 on 2020-04-17 19:56

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Model_Podataka', '0004_merge_20200417_2059'),
    ]

    operations = [
        migrations.CreateModel(
            name='Klinika',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naziv', models.TextField(default=None, max_length=500)),
                ('adresa', models.TextField(default=None, max_length=500)),
                ('opis', models.TextField(default=None, max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Sala',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('broj', models.TextField(default=None, max_length=500)),
                ('naziv', models.TextField(default=None, max_length=500)),
                ('id_klinike_kojoj_pripada', models.TextField(default=None, max_length=500)),
                ('opis', models.TextField(default=None, max_length=500)),
            ],
        ),
        migrations.AlterModelManagers(
            name='pacijent',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.RemoveField(
            model_name='lekar',
            name='adresa_prebivalista',
        ),
        migrations.RemoveField(
            model_name='lekar',
            name='drzava',
        ),
        migrations.RemoveField(
            model_name='lekar',
            name='grad',
        ),
        migrations.RemoveField(
            model_name='pacijent',
            name='id',
        ),
        migrations.AddField(
            model_name='lekar',
            name='datum',
            field=models.DateTimeField(default=None, max_length=500),
        ),
        migrations.AddField(
            model_name='lekar',
            name='pozicija',
            field=models.TextField(default=None, max_length=500),
        ),
        migrations.AddField(
            model_name='lekar',
            name='radno_mesto',
            field=models.TextField(default=None, max_length=500),
        ),
        migrations.AlterField(
            model_name='lekar',
            name='broja_telefona',
            field=models.TextField(default=None, max_length=500),
        ),
        migrations.AlterField(
            model_name='lekar',
            name='email_adresa',
            field=models.TextField(default=None, max_length=500),
        ),
        migrations.AlterField(
            model_name='lekar',
            name='ime',
            field=models.TextField(default=None, max_length=500),
        ),
        migrations.AlterField(
            model_name='lekar',
            name='jedinstveni_broj_osiguranika',
            field=models.TextField(default=None, max_length=500),
        ),
        migrations.AlterField(
            model_name='lekar',
            name='lozinka',
            field=models.TextField(default=None, max_length=500),
        ),
        migrations.AlterField(
            model_name='lekar',
            name='prezime',
            field=models.TextField(default=None, max_length=500),
        ),
        migrations.AlterField(
            model_name='pacijent',
            name='adresa_prebivalista',
            field=models.CharField(default=None, max_length=500),
        ),
        migrations.AlterField(
            model_name='pacijent',
            name='alergije_na_lek',
            field=models.CharField(default=None, max_length=500),
        ),
        migrations.AlterField(
            model_name='pacijent',
            name='broja_telefona',
            field=models.CharField(default=None, max_length=500),
        ),
        migrations.AlterField(
            model_name='pacijent',
            name='datum',
            field=models.DateTimeField(default=None, max_length=500),
        ),
        migrations.AlterField(
            model_name='pacijent',
            name='diagnoza',
            field=models.CharField(default=None, max_length=500),
        ),
        migrations.AlterField(
            model_name='pacijent',
            name='dioptrija',
            field=models.CharField(default=None, max_length=500),
        ),
        migrations.AlterField(
            model_name='pacijent',
            name='drzava',
            field=models.CharField(default=None, max_length=500),
        ),
        migrations.AlterField(
            model_name='pacijent',
            name='email_adresa',
            field=models.CharField(default=None, max_length=500, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='pacijent',
            name='grad',
            field=models.CharField(default=None, max_length=500),
        ),
        migrations.AlterField(
            model_name='pacijent',
            name='ime',
            field=models.CharField(default=None, max_length=500),
        ),
        migrations.AlterField(
            model_name='pacijent',
            name='jedinstveni_broj_osiguranika',
            field=models.CharField(default=None, max_length=500),
        ),
        migrations.AlterField(
            model_name='pacijent',
            name='krvna_grupa',
            field=models.CharField(default=None, max_length=3),
        ),
        migrations.AlterField(
            model_name='pacijent',
            name='lekovi',
            field=models.CharField(default=None, max_length=500),
        ),
        migrations.AlterField(
            model_name='pacijent',
            name='lozinka',
            field=models.CharField(default=None, max_length=500),
        ),
        migrations.AlterField(
            model_name='pacijent',
            name='prezime',
            field=models.CharField(default=None, max_length=500),
        ),
        migrations.AlterField(
            model_name='pacijent',
            name='sifra_bolesti',
            field=models.CharField(default=None, max_length=500),
        ),
        migrations.AlterField(
            model_name='pacijent',
            name='tezina',
            field=models.FloatField(default=None, max_length=500),
        ),
        migrations.AlterField(
            model_name='pacijent',
            name='visina',
            field=models.FloatField(default=None, max_length=500),
        ),
        migrations.AlterField(
            model_name='snippet',
            name='title',
            field=models.CharField(default=None, max_length=50),
        ),
    ]