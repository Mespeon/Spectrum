# Generated by Django 2.0 on 2018-01-16 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainboard', '0025_auto_20171222_1230'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesadvice',
            name='apBatchNumber',
            field=models.CharField(default='', max_length=20),
        ),
    ]