# Generated by Django 3.0.5 on 2020-05-08 18:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Model_Podataka', '0017_auto_20200508_1405'),
    ]

    operations = [
        migrations.AddField(
            model_name='pregled',
            name='temp',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 8, 20, 19, 19, 293037), max_length=500),
        ),
    ]