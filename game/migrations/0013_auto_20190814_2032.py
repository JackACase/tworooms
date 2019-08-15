# Generated by Django 2.2.1 on 2019-08-15 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0012_auto_20190729_1927'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playset',
            name='cards',
        ),
        migrations.RemoveField(
            model_name='game',
            name='playset',
        ),
        migrations.RemoveField(
            model_name='player',
            name='role',
        ),
        migrations.AddField(
            model_name='player',
            name='card_idx',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='state',
            field=models.CharField(default='waitingForPlayers', max_length=256),
        ),
        migrations.DeleteModel(
            name='Card',
        ),
        migrations.DeleteModel(
            name='Playset',
        ),
    ]
