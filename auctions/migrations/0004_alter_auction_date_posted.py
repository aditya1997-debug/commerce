# Generated by Django 4.0.4 on 2022-08-03 16:31

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_alter_auction_date_posted_alter_bid_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='date_posted',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 3, 16, 31, 55, 871487, tzinfo=utc)),
        ),
    ]