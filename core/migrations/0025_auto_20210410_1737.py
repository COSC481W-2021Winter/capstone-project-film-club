# Generated by Django 3.1.5 on 2021-04-10 21:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_reviewcomment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='friends',
            new_name='following',
        ),
    ]