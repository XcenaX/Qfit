# Generated by Django 3.1.6 on 2021-02-17 09:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20210216_2229'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timer',
            name='service',
        ),
        migrations.AlterField(
            model_name='timer',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 17, 15, 10, 41, 170092)),
        ),
        migrations.AlterField(
            model_name='traintimer',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 17, 15, 10, 41, 171090)),
        ),
    ]
