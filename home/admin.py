from django.contrib import admin
from .models import (
    CompanyEmail,
)


@admin.register(CompanyEmail)
class CompanyEmailAdmin(admin.ModelAdmin): 
    list_display = ['title', 'email']
    exclude = ['title']