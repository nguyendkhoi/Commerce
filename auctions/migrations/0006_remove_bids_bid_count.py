# Generated by Django 5.1.4 on 2025-01-01 15:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0005_remove_auctionlistings_bid_count_bids_bid_count"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="bids",
            name="bid_count",
        ),
    ]
