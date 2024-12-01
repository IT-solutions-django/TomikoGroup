from django import forms 
from django.db import models
from .models import (
    Product, 
    Category, 
    Brand, 
    ProductPhoto,
)


class FilterForm(forms.Form): 
    class SortingChoices(models.TextChoices):
        DEFAULT = 'default', 'исходная сортировка'
        POPULARITY = 'popularity', 'по популярности'
        RATING = 'rating', 'по рейтингу'
        NEWEST = 'new', 'по новизне'
        PRICE_ASC = 'price_asc', 'по возрастанию цены'
        PRICE_DESC = 'price_desc', 'по убыванию цены'

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), 
        widget=forms.RadioSelect(), 
        required=False) 
    sorting = forms.ChoiceField(
        choices=SortingChoices.choices,
        widget=forms.Select(), 
        required=False, 
    )