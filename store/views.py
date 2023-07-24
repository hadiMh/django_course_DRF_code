from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import F, ExpressionWrapper, DecimalField
from django.db import transaction

from .models import Category, Comment, Product, Customer, OrderItem, Order

@transaction.atomic()
def show_data(request):
    order = Order.objects.create(customer_id=1)

    order_item1 = OrderItem.objects.create(
        order=order,
        product_id=1,
        quantity=10,
        unit_price=1000,
    )

    return render(request, 'hello.html')

