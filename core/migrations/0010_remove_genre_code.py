# Generated by Django 3.1.5 on 2021-02-12 23:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20210212_1843'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='genre',
            name='code',
        ),
    ]
