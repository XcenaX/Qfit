# Generated by Django 3.1.7 on 2021-03-25 15:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0028_auto_20210320_1915'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='password',
        ),
        migrations.AlterField(
            model_name='timer',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 25, 15, 21, 42, 855949)),
        ),
        migrations.AlterField(
            model_name='traintimer',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 25, 15, 21, 42, 855949)),
        ),
    ]