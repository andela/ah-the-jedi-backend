# Generated by Django 2.1 on 2019-05-08 12:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0021_auto_20190508_1109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmarkarticlemodel',
            name='bookmarked_at',
            field=models.DateTimeField(auto_created=True, default=datetime.datetime.now),
        ),
    ]