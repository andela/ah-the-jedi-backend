# Generated by Django 2.1 on 2019-05-06 15:30

import autoslug.fields
import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
            ],
            options={
                'ordering': ['-createdAt'],
            },
        ),
        migrations.CreateModel(
            name='FavoriteArticleModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorited_article', to='articles.ArticleModel')),
            ],
        ),
    ]
