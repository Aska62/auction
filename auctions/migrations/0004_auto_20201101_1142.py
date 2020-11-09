# Generated by Django 3.1.1 on 2020-11-01 11:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20201101_1038'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='bidding',
        ),
        migrations.AddField(
            model_name='bidding',
            name='listing',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auctions.listing'),
        ),
    ]