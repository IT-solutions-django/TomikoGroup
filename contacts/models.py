from django.db import models


class Request(models.Model): 
    name = models.CharField('Имя', max_length=100) 
    phone = models.CharField('Телефон', max_length=18) 
    is_closed = models.BooleanField('Обработано', default=False)

    class Meta: 
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self) -> str: 
        return f'{"Обработано ✓" if self.is_closed else "Не обработано ✕"} | {self.name}, {self.phone}'