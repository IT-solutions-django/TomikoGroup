from django.forms import forms
from .models import (
    Request,
)


class RequestForm(forms.ModelForm): 
    class Meta:
        model = Request
        fields = ['name', 'phone']
        labels = {
            'name': 'Имя',
            'phone': 'Телефон',
        }