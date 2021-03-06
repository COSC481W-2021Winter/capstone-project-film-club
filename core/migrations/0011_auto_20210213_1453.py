# Generated by Django 3.1.5 on 2021-02-13 19:53

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0010_remove_genre_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='friends',
            field=models.ManyToManyField(blank=True, related_name='friends', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=1000)),
                ('genres', models.ManyToManyField(blank=True, related_name='movie_genres', to='core.Genre')),
            ],
        ),
        migrations.AddField(
            model_name='userprofile',
            name='watched_movies',
            field=models.ManyToManyField(blank=True, related_name='watched_movies', to='core.Movie'),
        ),
    ]
