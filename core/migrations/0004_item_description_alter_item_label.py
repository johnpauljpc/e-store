# Generated by Django 5.0 on 2023-12-15 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_item_discount_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='description',
            field=models.TextField(default='This is an amazing product'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='item',
            name='label',
            field=models.CharField(choices=[('New', 'primary'), ('S', 'secondary'), ('D', 'danger')], max_length=10),
        ),
    ]
