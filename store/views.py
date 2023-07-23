from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Count, Min, Max, Sum, Avg, F, Value, Func

from .models import Comment, Product, Customer, OrderItem, Order

def show_data(request):
    queryset = Customer.objects.annotate(orders_count=Count('orders'))
    print(queryset)
    return render(request, 'hello.html')


# expression

# Value - simple
# F
# Func
# Aggregate
# ExpressionWrapper
