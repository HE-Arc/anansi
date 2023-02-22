# Generated by Django 4.1.6 on 2023-02-22 01:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('anansiapp', '0003_alter_cardgame_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardgame',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
