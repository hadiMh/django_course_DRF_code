from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import F, ExpressionWrapper, DecimalField
from django.db import transaction, connection

from .models import Category, Comment, Product, Customer, OrderItem, Order


def show_data(request):
    cursor = connection.cursor()
    # cursor.execute('')
    # cursor.close()

    # with connection.cursor() as cursor:
    #     cursor.execute('')

    # Product.objects.raw('SELECT is, unit_price FROM store_product')

    # cursor.callproc('some_proc', 1, '2', 'hello')

    return render(request, 'hello.html')

