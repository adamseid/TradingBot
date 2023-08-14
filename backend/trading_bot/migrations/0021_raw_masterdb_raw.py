# Generated by Django 4.1.4 on 2023-05-04 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trading_bot', '0020_rename_timeframe_clientdata_timeframe'),
    ]

    operations = [
        migrations.CreateModel(
            name='Raw',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.CharField(default='', max_length=30)),
                ('price', models.CharField(default='', max_length=30)),
                ('volume', models.CharField(default='', max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='masterdb',
            name='raw',
            field=models.CharField(default='', max_length=30),
        ),
    ]