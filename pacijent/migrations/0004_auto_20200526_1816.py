# Generated by Django 3.0.5 on 2020-05-26 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pacijent', '0003_auto_20200524_1740'),
    ]

    operations = [
        migrations.AddField(
            model_name='operacije',
            name='ocenaKlinike',
            field=models.FloatField(default=-1),
        ),
        migrations.AddField(
            model_name='operacije',
            name='ocenaLekara',
            field=models.CharField(default='-1', max_length=500),
        ),
    ]