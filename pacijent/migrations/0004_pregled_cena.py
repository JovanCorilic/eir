# Generated by Django 3.0.5 on 2020-08-26 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pacijent', '0003_auto_20200823_0626'),
    ]

    operations = [
        migrations.AddField(
            model_name='pregled',
            name='cena',
            field=models.FloatField(default=1500.0),
        ),
    ]
