# Generated by Django 3.1.7 on 2021-11-29 15:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_auto_20211129_1328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='traintimer',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 29, 15, 36, 4, 949412)),
        ),
    ]