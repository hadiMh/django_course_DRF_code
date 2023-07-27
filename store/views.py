from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


@api_view()
def product_list(request):
    products_queryset = Product.objects.select_related('category').all()
    serializer = ProductSerializer(
        products_queryset, 
        many=True, 
        context={'request': request}
    )
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def product_detail(request, pk):
    if request.method == 'GET':
        product = get_object_or_404(
            Product.objects.select_related('category'),
            pk=pk
        )
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        return Response('All ok!')


@api_view()
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    serializer = CategorySerializer(category)
    return Response(serializer.data)
