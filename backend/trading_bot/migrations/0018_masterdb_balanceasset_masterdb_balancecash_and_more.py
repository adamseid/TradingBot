# Generated by Django 4.1.4 on 2023-04-25 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trading_bot', '0017_masterdb_dpricestdev'),
    ]

    operations = [
        migrations.AddField(
            model_name='masterdb',
            name='balanceAsset',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AddField(
            model_name='masterdb',
            name='balanceCash',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AddField(
            model_name='masterdb',
            name='value',
            field=models.CharField(default='', max_length=30),
        ),
    ]
