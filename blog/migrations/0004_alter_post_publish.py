# Generated by Django 3.2.9 on 2021-11-19 06:29

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20211119_0619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='publish',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 19, 6, 29, 10, 672531, tzinfo=utc)),
        ),
    ]
