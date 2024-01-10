# Generated by Django 4.0.4 on 2022-08-04 15:13

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_alter_auction_date_posted'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='date_posted',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 4, 15, 13, 2, 600666, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='auction',
            name='date_posted',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 4, 15, 13, 2, 599666, tzinfo=utc)),
        ),
    ]