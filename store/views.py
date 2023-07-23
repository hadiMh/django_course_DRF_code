from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q, F

from .models import Comment, Product, Customer, OrderItem, Order

def show_data(request):
    queryset = Order.objects.prefetch_related('items__product').select_related('customer').all()
    print(list(queryset))
    return render(request, 'hello.html', {'orders': list(queryset)})
