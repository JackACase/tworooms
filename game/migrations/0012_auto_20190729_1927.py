# Generated by Django 2.2.1 on 2019-07-29 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0011_auto_20190723_1902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='start_time',
            field=models.BigIntegerField(null=True),
        ),
    ]