# Generated by Django 5.1.3 on 2024-12-01 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_product_barcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='barcode',
            field=models.CharField(max_length=8, unique=True, verbose_name='Штрихкод'),
        ),
    ]
