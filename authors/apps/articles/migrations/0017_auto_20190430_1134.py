# Generated by Django 2.1 on 2019-04-30 11:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0016_auto_20190430_1123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlemodel',
            name='image',
            field=models.TextField(default='', max_length=1000, validators=[django.core.validators.URLValidator]),
        ),
    ]
