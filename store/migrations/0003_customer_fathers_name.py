# Generated by Django 4.2.3 on 2023-07-18 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_rename_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='fathers_name',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
