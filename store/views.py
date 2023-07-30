from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Prefetch
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny, DjangoModelPermissions

from .models import Cart, CartItem, Category, Comment, Customer, Order, OrderItem, Product
from .serializers import AddCartItemSerializer, CartItemSerializer, CartSerializer, CategorySerializer, CommentSerializer, CustomerSerializer, OrderCreateSerializer, OrderForAdminSerializer, OrderSerializer, OrderUpdateSerializer, ProductSerializer, UpdateCartItemSerializer
from .filters import ProductFilter
from .permissions import CustomDjangoModelPermissions, IsAdminOrReadOnly, SendPrivateEmailToCustomerPermission
from .signals import order_created


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['name', 'unit_price', 'inventory']
    search_fields = ['name', 'category__title']
    # pagination_class = DefaultPagination
    # filterset_fields = ['category_id', 'inventory']
    filterset_class = ProductFilter
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, pk):
        product = get_object_or_404(
            Product.objects.select_related('category'),
            pk=pk,
        )
        if product.order_items.count() > 0:
            return Response({'error': 'There is some order items including this product. Please remove them first.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.prefetch_related('products').all()
    permission_classes = [IsAdminOrReadOnly]

    def delete(self, request, pk):
        category = get_object_or_404(Category.objects.prefetch_related('products'), pk=pk)
        if category.products.count() > 0:
            return Response({'error': 'There is some products relating this category. Please remove them first.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        product_pk = self.kwargs['product_pk']
        return Comment.objects.filter(product_id=product_pk).all()
    
    def get_serializer_context(self):
        return {'product_pk': self.kwargs['product_pk']}
    

class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        cart_pk = self.kwargs['cart_pk']
        return CartItem.objects.select_related('product').filter(cart_id=cart_pk).all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer
    
    def get_serializer_context(self):
        return {'cart_pk': self.kwargs['cart_pk']}


class CartViewSet(CreateModelMixin,
                   RetrieveModelMixin,
                   DestroyModelMixin,
                   GenericViewSet):
    serializer_class = CartSerializer
    queryset = Cart.objects.prefetch_related('items__product').all()

class CustomerViewSet(ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        user_id = request.user.id
        customer = Customer.objects.get(user_id=user_id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

    @action(detail=True, permission_classes=[SendPrivateEmailToCustomerPermission])
    def send_private_email(self, request, pk):
        return Response(f'Sending email to customer {pk=}')


class OrderViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'options', 'head']

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        queryset = Order.objects.prefetch_related(
            Prefetch(
                'items',
                queryset=OrderItem.objects.select_related('product'),
            )
        ).select_related('customer__user').all()

        user = self.request.user

        if user.is_staff:
            return queryset
        
        return queryset.filter(customer__user_id=user.id)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateSerializer
        
        if self.request.method == 'PATCH':
            return OrderUpdateSerializer

        if self.request.user.is_staff:
            return OrderForAdminSerializer
        return OrderSerializer

    
    def create(self, request, *args, **kwargs):
        create_order_serializer = OrderCreateSerializer(
            data=request.data,
            context={'user_id': self.request.user.id},
        )
        create_order_serializer.is_valid(raise_exception=True)
        created_order = create_order_serializer.save()

        order_created.send_robust(self.__class__, order=created_order)

        serializer = OrderSerializer(created_order)
        return Response(serializer.data)
