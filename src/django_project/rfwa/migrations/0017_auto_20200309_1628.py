# Generated by Django 2.2.6 on 2020-03-09 16:28

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('rfwa', '0016_auto_20200305_1615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lab',
            name='close_Date',
            field=models.DateTimeField(verbose_name=datetime.datetime(2020, 3, 9, 16, 28, 47, 602065, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='lab',
            name='open_Date',
            field=models.DateTimeField(verbose_name=datetime.datetime(2020, 3, 9, 16, 28, 47, 602045, tzinfo=utc)),
        ),
    ]
