# Generated by Django 3.1.5 on 2021-03-07 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_userprofile_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_pic',
            field=models.ImageField(blank=True, default='person_icon.png', null=True, upload_to='users/'),
        ),
    ]
