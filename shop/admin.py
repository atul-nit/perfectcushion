from django.contrib import admin
from .models import Product, Category
from django.http import HttpResponse
import csv
from .product_analytics import get_product_list_name
from .product_analytics import get_all_products


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
    actions = ['get_products_list', 'get_all_products']
    list_display = ['id', 'name', 'slug', 'stock', 'popularity']
    prepopulated_fields = {'slug':('name',)}
    list_editable = ['stock']

    def get_products_list(self, request, queryset):
        field_names = ["ID", "Name"]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format("listnames")
        writer = csv.writer(response)
        writer.writerow(field_names)
        result = get_product_list_name()
        try:
            if result['actions_completed']:
                products_list = result['result']
                for item in products_list:
                    writer.writerow(item)
            else:
                raise Exception("All Actions not completed")
        except Exception as e:
            print(e)
        return response

    def get_all_products(self, request, queryset):
        print("Get all product called")
        field_names = ["Product Id", "Name", "Slug", "Price", "Stock"]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format("allprod")
        writer = csv.writer(response)
        writer.writerow(field_names)
        result = get_all_products()
        try:
            if result['actions_completed']:
                products_list = result['result']
                for item in products_list:
                    writer.writerow(item)
            else:
                raise Exception("All Actions not completed")
        except Exception as e:
            print(e)
        return response

    

admin.site.register(Product, ProductAdmin)