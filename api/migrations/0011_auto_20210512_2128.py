# Generated by Django 3.1.7 on 2021-05-12 21:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20210503_1344'),
    ]

    operations = [
        migrations.AddField(
            model_name='timer',
            name='book_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='traintimer',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 12, 21, 28, 10, 885884)),
        ),
    ]