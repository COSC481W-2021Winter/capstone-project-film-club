# Generated by Django 3.1.5 on 2021-02-12 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20210212_1815'),
    ]

    operations = [
        migrations.AddField(
            model_name='genre',
            name='api_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='genre',
            name='code',
            field=models.CharField(default='RO', max_length=3),
            preserve_default=False,
        ),
    ]