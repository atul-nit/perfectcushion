from django.contrib import admin
from django.http import HttpResponse
import csv
from .models import OrderItem, Order
from .order_analytics import get_order_list
from .order_analytics import get_order_three_months_old


class OrderItemAdmin(admin.TabularInline):
    model = OrderItem
    fieldsets = [
        ('Product', {'fields': ['product'],}),
        ('Quantity', {'fields': ['quantity'],}),
        ('Price', {'fields': ['price'],}),
    ]
    readonly_fields = ['product', 'quantity', 'price']
    can_delete = False
    max_num = 0
    template = 'admin/order/tabular.html'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    actions = ['get_order_list', 'get_order_list_three_months_old']
    list_display = ['id', 'billingName', 'email_address', 'created']
    list_display_links = ('id', 'billingName')
    search_fields = ['id', 'billingName', 'email_address']
    readonly_fields = ['id', 'token', 'total', 'email_address', 'created', 'billingName', 'billingAddress1',
                       'billingCity', 'billingPostcode', 'billingCountry', 'shippingName', 'shippingAddress1',
                       'shippingCity', 'shippingPostcode', 'shippingCountry']
    fieldsets = [
        ('ORDER INFORMATION', {'fields': ['id', 'token', 'total', 'created']}),
        ('BILLING INFORMATION', {'fields': ['billingName', 'billingAddress1', 'billingCity',
                                            'billingPostcode', 'billingCountry', 'email_address']}),
        ('SHIPPING INFORMATION', {'fields': ['shippingName', 'shippingAddress1', 'shippingCity',
                                             'shippingPostcode', 'shippingCountry']}),
    ]

    inlines = [
        OrderItemAdmin,
    ]

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def get_order_list(self, request, queryset):
        field_names = ["Order ID", "Order Value", "Customer Email", "Order Created At"]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format("orderlist")
        writer = csv.writer(response)
        writer.writerow(field_names)
        result = get_order_list()
        orders_list = result["result"]
        for item in orders_list:
            writer.writerow(item)
        return response

    def get_order_list_three_months_old(self, request, queryset):
        field_names = ["Order ID", "Order Value", "Customer Email", "Order Created At"]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format("orderlist_3months_old")
        writer = csv.writer(response)
        writer.writerow(field_names)
        result = get_order_three_months_old()
        orders_list = result["result"]
        for item in orders_list:
            writer.writerow(item)
        return response