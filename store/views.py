from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Product
from .serializers import ProductSerializer


@api_view()
def product_list(request):
    products_queryset = Product.objects.select_related('category').all()
    serializer = ProductSerializer(products_queryset, many=True)
    return Response(serializer.data)


@api_view()
def product_detail(request, id):
    product = get_object_or_404(
        Product.objects.select_related('category'),
        pk=id
    )
    serializer = ProductSerializer(product)
    return Response(serializer.data)
