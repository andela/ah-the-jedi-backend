# Generated by Django 2.1 on 2019-05-08 12:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0022_auto_20190508_1237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmarkarticlemodel',
            name='bookmarked_at',
            field=models.DateTimeField(auto_created=True, default=django.utils.timezone.now),
        ),
    ]
