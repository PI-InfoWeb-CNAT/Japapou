# Generated by Django 5.2.3 on 2025-07-25 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('japapou', '0012_order_orderitem_plateoption'),
    ]

    operations = [
        migrations.AddField(
            model_name='plate',
            name='options',
            field=models.ManyToManyField(blank=True, to='japapou.plateoption'),
        ),
    ]
