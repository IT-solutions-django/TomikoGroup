# Generated by Django 5.1.3 on 2024-12-09 09:21

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Оценка')),
                ('content', models.TextField(verbose_name='Содержание')),
                ('created_at', models.DateTimeField(verbose_name='Дата и время публикации')),
                ('platform', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.reviewplatform', verbose_name='Платформа')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
                'ordering': ['-created_at'],
            },
        ),
    ]