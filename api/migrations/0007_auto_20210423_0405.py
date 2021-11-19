# Generated by Django 3.1.7 on 2021-04-23 04:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20210423_0138'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servicecategory',
            name='image_url',
        ),
        migrations.AddField(
            model_name='traintimer',
            name='transaction_id',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='avatar',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='myimage',
            name='image',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='servicecategory',
            name='image',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='traintimer',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 23, 4, 5, 33, 753272)),
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
