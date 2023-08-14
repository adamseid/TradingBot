# Generated by Django 4.1.4 on 2023-03-17 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trading_bot', '0005_masterdb_stdev_masterdb_trend'),
    ]

    operations = [
        migrations.RenameField(
            model_name='masterdb',
            old_name='stdev',
            new_name='momentumStdev',
        ),
        migrations.AddField(
            model_name='masterdb',
            name='trendStdev',
            field=models.CharField(default='', max_length=30),
        ),
    ]
