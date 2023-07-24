from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import F, ExpressionWrapper, DecimalField
from django.db import transaction

from .models import Category, Comment, Product, Customer, OrderItem, Order


def show_data(request):
    queryset = Product.objects.all()
    print(queryset[2:4])

    list(queryset)

    return render(request, 'hello.html')

