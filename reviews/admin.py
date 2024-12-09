from django.contrib import admin
from .models import (
    Review, 
    ReviewPlatform
)


@admin.register(Review) 
class CategoryAdmin(admin.ModelAdmin): 
    list_display = ['pk', 'content', 'created_at']