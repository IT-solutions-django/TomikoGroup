from django.urls import path
from .views import *


app_name = 'products'


urlpatterns = [
    path('catalog', CatalogView.as_view(), name='catalog'),
    path('doctor/<slug:product_slug>/', ProductView.as_view(), name='product')
]