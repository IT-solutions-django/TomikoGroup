from django.urls import path
from .views import *


app_name = 'products'


urlpatterns = [
    path('catalog', CatalogView.as_view(), name='catalog'),
]