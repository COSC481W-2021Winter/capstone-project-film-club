# Generated by Django 3.1.5 on 2021-04-18 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_auto_20210417_0552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_bio',
            field=models.CharField(blank=True, default='This is your bio.', max_length=150),
        ),
    ]