# Generated by Django 2.2.19 on 2021-03-12 13:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_auto_20210304_1232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timer',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 12, 13, 47, 25, 856104)),
        ),
        migrations.AlterField(
            model_name='traintimer',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 12, 13, 47, 25, 857101)),
        ),
    ]
