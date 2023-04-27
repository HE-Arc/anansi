# Generated by Django 4.1.6 on 2023-04-27 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anansiapp', '0017_remove_round_round_response_card_winner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='creator',
        ),
        migrations.RemoveField(
            model_name='game',
            name='winner',
        ),
        migrations.AddField(
            model_name='gameplayer',
            name='is_game_creator',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='gameplayer',
            name='is_game_winner',
            field=models.BooleanField(default=False),
        ),
    ]
