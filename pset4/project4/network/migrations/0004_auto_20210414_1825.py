# Generated by Django 3.1.5 on 2021-04-14 18:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_likes_post'),
    ]

    operations = [
        migrations.RenameField(
            model_name='likes',
            old_name='post',
            new_name='liked',
        ),
        migrations.RenameField(
            model_name='likes',
            old_name='user',
            new_name='liker',
        ),
    ]
