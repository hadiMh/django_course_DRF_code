from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Count, Min, Max, Sum, Avg, F, Value, Func

from .models import Comment, Product, Customer, OrderItem, Order

def show_data(request):
    queryset = Customer.objects \
                            .annotate(fullname=Func(
                                F('first_name'),
                                Value(' '),
                                F('last_name'),
                                function='CONCAT'
                            )) \
                            .defer('first_name', 'last_name')
    print(queryset)
    return render(request, 'hello.html')


# expression

# Value - simple
# F
# Func
# Aggregate
# ExpressionWrapper
