# Generated by Django 4.1.4 on 2023-04-13 17:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trading_bot', '0015_rename_selectionmenu_clientdata_selection_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clientdata',
            old_name='selectionList',
            new_name='location',
        ),
    ]
