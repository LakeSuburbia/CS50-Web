# Generated by Django 3.1.5 on 2021-02-10 18:04

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0024_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='watchlist',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
