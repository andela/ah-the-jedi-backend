# Generated by Django 2.1 on 2019-05-09 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('highlights', '0002_auto_20190507_2120'),
    ]

    operations = [
        migrations.AddField(
            model_name='highlightsmodel',
            name='location',
            field=models.CharField(default='body', max_length=200),
            preserve_default=False,
        ),
    ]
