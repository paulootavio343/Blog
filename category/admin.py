from django.contrib import admin
from .models import Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name', 'category_slug')
    list_display_links = ('id', 'category_name')


admin.site.register(Category, CategoryAdmin)
