# Generated by Django 3.1.5 on 2021-02-02 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_remove_listing_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='image',
            field=models.ImageField(default='images/image-not-found.jpg', upload_to=''),
        ),
    ]
