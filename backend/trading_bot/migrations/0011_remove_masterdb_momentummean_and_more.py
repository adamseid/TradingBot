# Generated by Django 4.1.4 on 2023-03-23 13:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trading_bot', '0010_masterdb_momentummean'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='masterdb',
            name='momentumMean',
        ),
        migrations.RemoveField(
            model_name='masterdb',
            name='volatility',
        ),
    ]
