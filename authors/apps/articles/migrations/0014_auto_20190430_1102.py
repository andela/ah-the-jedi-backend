# Generated by Django 2.1 on 2019-04-30 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0013_auto_20190429_2028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlemodel',
            name='slug',
            field=models.SlugField(default='djangodbmodelsfieldscharfield', unique=True),
        ),
    ]
