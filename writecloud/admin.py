from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Story)
admin.site.register(Page)

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('value', 'comment', 'user', 'story')
    search_fields = ('user', 'story')
