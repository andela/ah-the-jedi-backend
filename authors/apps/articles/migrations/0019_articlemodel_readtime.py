# Generated by Django 2.2 on 2019-05-07 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0018_auto_20190501_0942'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlemodel',
            name='readtime',
            field=models.CharField(default=1, max_length=240),
            preserve_default=False,
        ),
    ]
