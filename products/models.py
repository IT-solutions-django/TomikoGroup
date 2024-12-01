from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import os


class Brand(models.Model): 
    title = models.CharField('Название', max_length=60, null=False)

    class Meta: 
        verbose_name = 'бренд'
        verbose_name_plural = 'бренды'

    def __str__(self) -> str: 
        return self.title
    

class Category(models.Model): 
    title = models.CharField('Название', max_length=80, null=False, unique=True)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self) -> str: 
        return self.title


class Product(models.Model): 
    barcode = models.CharField('Штрихкод', unique=True, max_length=8) 
    brand = models.ForeignKey(Brand, verbose_name='Бренд', on_delete=models.CASCADE, null=False, related_name='products') 
    title = models.CharField('Название', max_length=200, null=False) 
    description = models.TextField('Описание', null=True, blank=True) 
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE, null=True, related_name='categories')
    volume = models.CharField('Объём', max_length=100, null=True, blank=True) 
    weight = models.DecimalField('Вес', decimal_places=2, max_digits=4, null=True, blank=True,
                                 validators=(MinValueValidator(Decimal(0), 'Вес не может быть отрицательным'),))
    notes = models.CharField('Заметки', max_length=30, null=True, blank=True)
    price = models.DecimalField('Цена', decimal_places=2, max_digits=10, 
                                validators=[MinValueValidator(Decimal(0), 'Цена не может быть отрицательной')]) 
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta: 
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self) -> str:
        return f'{self.title}'
    

class ProductPhoto(models.Model):
    image = models.ImageField('Изображение', upload_to='products', null=True, blank=True)
    product = models.ForeignKey(verbose_name='Товар', to=Product, on_delete=models.CASCADE, related_name='photos', null=True)
    created_at = models.DateTimeField('Дата загрузки', auto_now_add=True)

    class Meta: 
        verbose_name = 'фото'
        verbose_name_plural = 'фото товара'

    def __str__(self) -> str:
        return f'{self.image}'
    
    def save(self, *args, **kwargs):
        if self.pk:  
            old_image = ProductPhoto.objects.filter(pk=self.pk).first().image
            if old_image and self.image and old_image.name == self.image.name:
                super(ProductPhoto, self).save(*args, **kwargs)
                return
            
        image_name = os.path.splitext(os.path.basename(self.image.name))[0].lower() 
        img = Image.open(self.image)
        img_io = BytesIO()
        img.save(img_io, format="WebP")
        img_file = InMemoryUploadedFile(
            file=img_io,
            field_name=None,
            name=f"{image_name}.webp",
            content_type="image/webp",
            size=img_io.tell(),
            charset=None,
        )
        self.image.save(f"{image_name}.webp", img_file, save=False)
        super(ProductPhoto, self).save(*args, **kwargs)