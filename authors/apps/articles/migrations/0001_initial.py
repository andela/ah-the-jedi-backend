# Generated by Django 2.1 on 2019-05-02 08:49

import autoslug.fields
from django.conf import settings
import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, blank=True, editable=False, null=True, populate_from='title', unique=True)),
                ('title', models.CharField(max_length=254)),
                ('description', models.TextField()),
                ('body', models.TextField()),
                ('tagList', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(max_length=128), blank=True, default=list, size=None)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now_add=True)),
                ('favorited', models.BooleanField(default=False)),
                ('favoritesCount', models.IntegerField(default=0)),
                ('image', models.TextField(default='', max_length=1000, validators=[django.core.validators.URLValidator])),
                ('author', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='article_author', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-createdAt'],
            },
        ),
    ]
