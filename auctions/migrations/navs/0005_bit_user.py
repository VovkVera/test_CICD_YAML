# Generated by Django 3.0.5 on 2020-07-29 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_remove_bit_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='bit',
            name='user',
            field=models.CharField(default='Some one', max_length=64),
        ),
    ]
