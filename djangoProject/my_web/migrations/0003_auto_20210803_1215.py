# Generated by Django 3.2.3 on 2021-08-03 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_web', '0002_auto_20210802_2229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statusrecord',
            name='bb_wager',
            field=models.IntegerField(default=100),
        ),
        migrations.AlterField(
            model_name='statusrecord',
            name='sb_wager',
            field=models.IntegerField(default=50),
        ),
    ]
