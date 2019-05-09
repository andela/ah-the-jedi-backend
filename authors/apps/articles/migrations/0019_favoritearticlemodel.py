# Generated by Django 2.1 on 2019-05-07 14:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('articles', '0018_auto_20190501_0942'),
    ]

    operations = [
        migrations.CreateModel(
            name='FavoriteArticleModel',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                              related_name='favorited_article', to='articles.ArticleModel')),
                ('favoritor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                                related_name='favorites', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
