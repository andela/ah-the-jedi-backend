# Generated by Django 2.2 on 2019-05-17 12:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0008_remove_reportmodel_reporter'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reportmodel',
            options={'ordering': ['-created_at']},
        ),
        migrations.RenameField(
            model_name='reportmodel',
            old_name='createdAt',
            new_name='created_at',
        ),
    ]
