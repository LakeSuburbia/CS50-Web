# Generated by Django 3.1.5 on 2021-02-03 09:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_listing_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='image',
        ),
    ]
