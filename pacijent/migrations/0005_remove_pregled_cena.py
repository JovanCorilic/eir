# Generated by Django 3.0.5 on 2020-08-26 13:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pacijent', '0004_pregled_cena'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pregled',
            name='cena',
        ),
    ]
