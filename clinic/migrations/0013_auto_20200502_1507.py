# Generated by Django 3.0.5 on 2020-05-02 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Model_Podataka', '0012_auto_20200501_1015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pacijent',
            name='datum',
            field=models.DateTimeField(default=None, max_length=500),
        ),
    ]
