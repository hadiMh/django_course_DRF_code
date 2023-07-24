from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import F, ExpressionWrapper, DecimalField

from .models import Category, Comment, Product, Customer, OrderItem, Order

def show_data(request):
    # Category.objects.filter(pk=102).delete()

    cat = Category(pk=102)
    cat.delete()

    return render(request, 'hello.html')

