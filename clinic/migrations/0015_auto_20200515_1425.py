# Generated by Django 3.0.5 on 2020-05-15 14:25

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Model_Podataka', '0014_odmor_pregled'),
    ]

    operations = [
        
        migrations.AddField(
            model_name='odmor',
            name='aktiviran',
            field=models.IntegerField(default=0),
        ),
    ]
