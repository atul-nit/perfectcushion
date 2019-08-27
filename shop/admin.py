from django.contrib import admin
from .models import Product, Category

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']
    prepopulated_fields = {'slug':('name',)}
    ordering = ['id']
    list_display_links = ['id', 'name']
admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'stock']
    prepopulated_fields = {'slug':('name',)}
    list_editable = ['stock']
admin.site.register(Product, ProductAdmin)