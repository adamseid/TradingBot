# Generated by Django 4.1.4 on 2023-07-07 04:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trading_bot', '0025_masterdb_balanceshort'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='masterdb',
            name='balanceShort',
        ),
    ]
