from typing import Any, List, Optional, Tuple
from django.contrib import admin, messages
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.db.models import Count, Prefetch
from django.utils.html import format_html
from django.urls import reverse
from django.utils.http import urlencode

from .models import Category, Comment, Customer, Order, OrderItem, Product


class InventoryFilter(admin.SimpleListFilter):
    LESS_THAN_3 = '<3'
    BETWEEN_3_and_10 = '3<=10'
    MORE_THAN_10 = '>10'
    title = 'Critical Inventory Status'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            (InventoryFilter.LESS_THAN_3, 'High'),
            (InventoryFilter.BETWEEN_3_and_10, 'Medium'),
            (InventoryFilter.MORE_THAN_10, 'OK'),
        ]
    
    def queryset(self, request, queryset):
        if self.value() == InventoryFilter.LESS_THAN_3:
            return queryset.filter(inventory__lt=3)
        if self.value() == InventoryFilter.BETWEEN_3_and_10:
            return queryset.filter(inventory__range=(3, 10))
        if self.value() == InventoryFilter.MORE_THAN_10:
            return queryset.filter(inventory__gt=10)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'inventory', 'unit_price', 'inventory_status', 'product_category', 'num_of_comments']
    list_per_page = 10
    list_editable = ['unit_price']
    list_select_related = ['category']
    list_filter = ['datetime_created', InventoryFilter]
    actions = ['clear_inventory']
    search_fields = ['name', ]
    prepopulated_fields = {
        'slug': ['name', ]
    }

    def get_queryset(self, request):
        return super().get_queryset(request) \
                .prefetch_related('comments') \
                .annotate(
                    comments_count=Count('comments'),
                )

    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        if product.inventory > 50:
            return 'High'
        return 'Medium'
    
    @admin.display(description='# comments', ordering='comments_count')
    def num_of_comments(self, product):
        url = (
            reverse('admin:store_comment_changelist') 
            + '?'
            + urlencode({
                'product__id': product.id,
            })
        )
        return format_html('<a href="{}">{}</a>', url, product.comments_count)
        
    
    @admin.display(ordering='category__title')
    def product_category(self, product):
        return product.category.title

    
    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        update_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{update_count} of products inventories cleared to zero.',
            messages.ERROR,
        )
    

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'status', ]
    list_editable = ['status']
    list_per_page = 10
    autocomplete_fields = ['product', ]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ['product', 'quantity', 'unit_price']
    extra = 0
    min_num = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'status', 'datetime_created', 'num_of_items']
    list_editable = ['status']
    list_per_page = 10
    ordering = ['-datetime_created']
    inlines = [OrderItemInline]

    def get_queryset(self, request):
        return super() \
                .get_queryset(request) \
                .prefetch_related('items') \
                .annotate(
                    items_count=Count('items')
                )

    @admin.display(ordering='items_count', description='# items')
    def num_of_items(self, order):
        return order.items_count

admin.site.register(Category)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', ]
    list_per_page = 10
    ordering = ['last_name', 'first_name', ]
    search_fields = ['first_name__istartswith', 'last_name__istartswith', ]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'unit_price']
    autocomplete_fields = ['product', ]
