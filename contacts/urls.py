from django.urls import path
from .views import *


app_name = 'contacts'


urlpatterns = [
    path('api/save-request/', SaveRequestView.as_view(), name='save_request'), 
]