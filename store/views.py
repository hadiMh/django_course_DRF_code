from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


class ProductList(ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.select_related('category').all()

    # def get_serializer_class(self):
    #     return ProductSerializer
    
    # def get_queryset(self):
    #     return Product.objects.select_related('category').all()

    def get_serializer_context(self):
        return {'request': self.request}


class ProductDetail(APIView):
    def get(self, request, pk):
        product = get_object_or_404(
            Product.objects.select_related('category'),
            pk=pk,
        )
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)
    
    def put(self, request, pk):
        product = get_object_or_404(
            Product.objects.select_related('category'),
            pk=pk,
        )
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, pk):
        product = get_object_or_404(
            Product.objects.select_related('category'),
            pk=pk,
        )
        if product.order_items.count() > 0:
            return Response({'error': 'There is some order items including this product. Please remove them first.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryList(ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.prefetch_related('products').all()


class CategoryDetail(APIView):
    def get(self, request, pk):
        category = get_object_or_404(Category.objects.prefetch_related('products'), pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, pk):
        category = get_object_or_404(Category.objects.prefetch_related('products'), pk=pk)
        serializer = CategorySerializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, pk):
        category = get_object_or_404(Category.objects.prefetch_related('products'), pk=pk)
        if category.products.count() > 0:
            return Response({'error': 'There is some products relating this category. Please remove them first.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        