# Generated by Django 5.0 on 2024-01-06 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_order_coupon'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='amount',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
