from django.contrib import admin
from .models import TravelPost

@admin.register(TravelPost)
class TravelPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('title', 'content')

  