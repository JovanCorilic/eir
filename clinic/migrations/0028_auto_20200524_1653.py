# Generated by Django 3.0.5 on 2020-05-24 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Model_Podataka', '0027_auto_20200518_2233'),
    ]

    operations = [
        migrations.AddField(
            model_name='klinika',
            name='ocena',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='lekar',
            name='ocena',
            field=models.IntegerField(default=-1),
        ),
    ]
