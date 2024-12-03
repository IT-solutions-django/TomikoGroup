from django.db import models


class CompanyEmail(models.Model): 
    email = models.EmailField('Почтовый адрес', max_length=100)

    title = models.TextField(
         'Email', 
        help_text='Название вкладки в админ. панели',
        default='Контактная информация'
    )

    class Meta: 
        verbose_name = 'email'
        verbose_name_plural = 'email'

    def save(self, *args, **kwargs):
        if self.__class__.objects.count():
            self.pk = self.__class__.objects.first().pk
        super().save(*args, **kwargs)

    @classmethod
    def get_instance(cls) -> "CompanyEmail":
        instance, created = cls.objects.get_or_create(id=1)
        return instance
    
    def __str__(self) -> str: 
        return f'Email {self.email}'