# Generated by Django 5.1.3 on 2024-12-01 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_alter_productphoto_options_remove_product_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(default='', verbose_name='Слаг'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(default='', verbose_name='Слаг'),
            preserve_default=False,
        ),
    ]