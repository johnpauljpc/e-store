# Generated by Django 5.0 on 2024-01-06 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_alter_item_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(default='items/imagePL.svg', upload_to='items/'),
        ),
    ]
