# Generated by Django 5.2 on 2025-05-07 09:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myroomieApp', '0003_profile_bio_roommember'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='room',
        ),
    ]
