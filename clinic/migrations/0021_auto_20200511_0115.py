# Generated by Django 3.0.5 on 2020-05-11 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Model_Podataka', '0020_pacijent_aktiviran'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pacijent',
            name='aktiviran',
            field=models.IntegerField(default=1),
        ),
    ]