# Generated by Django 5.0.3 on 2024-10-06 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hotel', '0002_rename_price_per_night_room_price_per_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='adults',
            field=models.IntegerField(default=2),
        ),
        migrations.AddField(
            model_name='room',
            name='children',
            field=models.IntegerField(default=3),
        ),
        migrations.AddField(
            model_name='room',
            name='rooms',
            field=models.IntegerField(default=3),
        ),
    ]