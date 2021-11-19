# Generated by Django 3.1.7 on 2021-04-23 01:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20210422_2237'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicecategory',
            name='image_url',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='traintimer',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 23, 1, 38, 58, 51926)),
        ),
    ]