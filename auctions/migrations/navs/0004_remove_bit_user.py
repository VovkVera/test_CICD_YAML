# Generated by Django 3.0.5 on 2020-07-29 13:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20200729_1319'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bit',
            name='user',
        ),
    ]