# Generated by Django 3.1.7 on 2021-04-20 18:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='traintimer',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 20, 18, 51, 27, 588819)),
        ),
    ]
