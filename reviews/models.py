from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class ReviewPlatform(models.Model): 
    name = models.CharField('Название', max_length=50)

    def __str__(self): 
        return self.name 
    
    class Meta: 
        verbose_name = 'платформа'
        verbose_name_plural = 'платформы'


class Review(models.Model): 
    rate = models.SmallIntegerField('Оценка', validators=[
        MinValueValidator(1), 
        MaxValueValidator(5)
    ])
    content = models.TextField('Содержание')
    created_at = models.DateTimeField('Дата и время публикации')
    platform = models.ForeignKey(verbose_name='Платформа', to=ReviewPlatform, on_delete=models.CASCADE)

    class Meta: 
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']

    def __str__(self) -> str: 
        return self.content[:20]