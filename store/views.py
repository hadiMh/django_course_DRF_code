from django.shortcuts import render
from django.http import HttpResponse

from .models import Product

def show_data(request):
    queryset = Product.objects.filter(id=1005) # [p1]
    print(queryset.exists())
    # product = queryset.first()
    # print(product.id)
    # print(product.name)
    # print(product.unit_price)

    return render(request, 'hello.html')
