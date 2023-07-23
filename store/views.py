from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import F, ExpressionWrapper, DecimalField

from .models import Comment, Product, Customer, OrderItem, Order

def show_data(request):
    queryset = Comment.approved.filter(datetime_created__year=2022).all()
    print(queryset)
    return render(request, 'hello.html')


# expression

# Value - simple
# F
# Func
# Aggregate
# ExpressionWrapper
