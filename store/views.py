from django.db import transaction, connection
from django.db.models import F, ExpressionWrapper, DecimalField
from django.http import HttpResponse
from django.shortcuts import render

from .models import Category, Comment, Product, Customer, OrderItem, Order


def show_data(request):
    return render(request, 'hello.html')

