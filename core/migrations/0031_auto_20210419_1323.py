# Generated by Django 3.1.5 on 2021-04-19 17:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0030_userprofile_isprivate'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='isPrivate',
            new_name='is_private',
        ),
    ]