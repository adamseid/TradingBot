# Generated by Django 4.1.4 on 2023-03-17 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trading_bot', '0006_rename_stdev_masterdb_momentumstdev_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='masterdb',
            name='volatility',
            field=models.CharField(default='', max_length=30),
        ),
    ]
