# Generated by Django 3.1.5 on 2021-04-02 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_merge_20210329_1515'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='liked_reviews',
            field=models.ManyToManyField(blank=True, related_name='liked_reviews', to='core.Review'),
        ),
    ]