# Generated by Django 5.0.3 on 2024-10-07 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hotel', '0004_rename_children_room_capacity_remove_room_adults'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=10000, max_digits=10),
        ),
    ]