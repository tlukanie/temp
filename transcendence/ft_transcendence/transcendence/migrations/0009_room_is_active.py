# Generated by Django 5.1.2 on 2024-11-18 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transcendence', '0008_room'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]