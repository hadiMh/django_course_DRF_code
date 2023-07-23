from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import F, ExpressionWrapper, DecimalField

from .models import Comment, Product, Customer, OrderItem, Order

def show_data(request):
    
    return render(request, 'hello.html')

