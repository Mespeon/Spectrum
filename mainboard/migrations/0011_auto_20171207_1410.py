# Generated by Django 2.0 on 2017-12-07 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainboard', '0010_auto_20171207_1410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='item_SKU',
            field=models.IntegerField(unique=True),
        ),
    ]
