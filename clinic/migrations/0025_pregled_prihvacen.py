# Generated by Django 3.0.5 on 2020-05-16 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Model_Podataka', '0024_auto_20200516_0622'),
    ]

    operations = [
        migrations.AddField(
            model_name='pregled',
            name='prihvacen',
            field=models.CharField(default='da', max_length=500),
        ),
    ]
