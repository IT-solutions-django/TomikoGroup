from django.db import models


class VkClipInfo(models.Model):
    """Модель описывающая платформу, где хранятся клипы"""

    clip_url = models.TextField(
        unique=True,
        verbose_name="ссылка на клип",
    )

    class Meta:
        verbose_name = "ссылка на вк клип"
        verbose_name_plural = "ссылки на вк клипы"

    def __str__(self):
        return self.clip_url


class Clip(models.Model):
    url = models.TextField(verbose_name="ссылка", help_text="ссылка в формате http/...")
    
    """Модель описывающая VK клип"""

    name = models.CharField(
        max_length=255,
        verbose_name="название",
        help_text="максимальная длина 255 символов",
    )

    vk_id = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="VK id",
        help_text="максимальная длина 255 символов",
    )

    thumbnail_url = models.TextField(
        verbose_name="ссылка на миниатюру", help_text="ссылка в формате http/..."
    )

    view_count = models.PositiveIntegerField(
        verbose_name="число просмотров", help_text="положительное число"
    )

    adding_date = models.DateTimeField(verbose_name="дата добавления")

    class Meta:
        verbose_name = "клип"
        verbose_name_plural = "клипы"
        ordering = ("-adding_date",)

    def __str__(self):
        return f"{self.name} {self.vk_id}"