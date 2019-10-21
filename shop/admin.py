from django.contrib import admin
from .models import Product, Category


class CatItemAdmin(admin.TabularInline):
    model = Product
    fieldsets = [
        ('Product', {'fields': ['name'], }),
        ('Price', {'fields': ['price'], }),
    ]
    readonly_fields = ['name', 'price']
    can_delete = False # to remove delete option
    max_num = 0 # to remove add option
    template = 'admin/shop/tabular.html'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']
    prepopulated_fields = {'slug':('name',)}
    ordering = ['id']
    list_display_links = ['id', 'name']

    inlines = [
        CatItemAdmin,
    ]
admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'stock']
    prepopulated_fields = {'slug':('name',)}
    list_editable = ['stock']
admin.site.register(Product, ProductAdmin)