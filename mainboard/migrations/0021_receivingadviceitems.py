# Generated by Django 2.0 on 2017-12-20 06:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainboard', '0020_receivingadvice'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReceivingAdviceItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('itemQty', models.IntegerField(default=0)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainboard.Product')),
                ('receiptNumber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainboard.ReceivingAdvice')),
            ],
        ),
    ]