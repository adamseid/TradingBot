# Generated by Django 4.1.4 on 2023-04-13 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trading_bot', '0014_remove_masterdb_trend_remove_masterdb_trendstdev'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clientdata',
            old_name='selectionMenu',
            new_name='selection',
        ),
        migrations.AddField(
            model_name='clientdata',
            name='selectionList',
            field=models.CharField(default='', max_length=30),
        ),
    ]
