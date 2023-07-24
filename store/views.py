from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import F, ExpressionWrapper, DecimalField

from .models import Category, Comment, Product, Customer, OrderItem, Order

def show_data(request):
    # category = Category.objects.get(pk=98)
    # category.title = 'Laptops'
    # category.top_product_id = 3
    # category.save()

    Category.objects.filter(pk__in=[96,95,94]).update(title='B')

    return render(request, 'hello.html')

