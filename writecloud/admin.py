from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(UserProfile)

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'author', 'length', 'uuid')
    search_fields = ('author', 'title', 'uuid')


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('story', 'number', 'author', 'content')
    search_fields = ('author', 'story')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('story', 'author', 'stars', 'body')
    search_fields = ('author', 'story')
