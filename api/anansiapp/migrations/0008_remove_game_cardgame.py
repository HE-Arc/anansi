# Generated by Django 4.1.6 on 2023-03-22 16:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('anansiapp', '0007_game_gameplayer_game_creator_game_winner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='cardgame',
        ),
    ]
