# Generated by Django 4.1.7 on 2023-03-08 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anansiapp', '0006_alter_cardgame_privacy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardgame',
            name='privacy',
            field=models.CharField(choices=[('public', 'Public'), ('private', 'Private')], max_length=10),
        ),
    ]