from decimal import Decimal
from django.utils.text import slugify
from rest_framework import serializers

from .models import Cart, CartItem, Category, Comment, Customer, Order, OrderItem, Product


class CategorySerializer(serializers.ModelSerializer):
    # num_of_products = serializers.SerializerMethodField()
    num_of_products = serializers.IntegerField(source='products.count', read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'title', 'description', 'num_of_products']

    # def get_num_of_products(self, category):
    #     return category.products.count()


class ProductSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255, source='name')
    price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    unit_price_after_tax = serializers.SerializerMethodField()
        
    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'category', 'unit_price_after_tax', 'inventory', 'description']
    
    def get_unit_price_after_tax(self, product):
        return round(product.unit_price * Decimal(1.09), 2)
    
    def validate(self, data):
        if len(data['name']) < 6:
            raise serializers.ValidationError('Product title length should be at least 6.')
        return data
    
    def create(self, validated_data):
        product = Product(**validated_data)
        product.slug = slugify(product.name)
        product.save()
        return product


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'name', 'body']

    def create(self, validated_data):
        product_id = self.context['product_pk']
        return Comment.objects.create(product_id=product_id, **validated_data)


class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'unit_price']


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']


class AddCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']

    def create(self, validated_data):
        cart_id = self.context['cart_pk']

        product = validated_data.get('product')
        quantity = validated_data.get('quantity')

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product.id)
            cart_item.quantity += quantity
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(cart_id=cart_id, **validated_data)

        self.instance = cart_item
        return cart_item


class CartItemSerializer(serializers.ModelSerializer):
    product = CartProductSerializer()
    item_total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'item_total']

    def get_item_total(self, cart_item):
        return cart_item.quantity * cart_item.product.unit_price


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']
        read_only_fields = ['id', ]

    def get_total_price(self, cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'user', 'birth_date']
        read_only_fields = ['user']


class OrderCustomerSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=255, source='user.first_name')
    last_name = serializers.CharField(max_length=255, source='user.last_name')
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'email']


class OrderItemProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'unit_price']


class OrderItemSerializer(serializers.ModelSerializer):
    product = OrderItemProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'unit_price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'status', 'datetime_created', 'items']


class OrderForAdminSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    customer = OrderCustomerSerializer()

    class Meta:
        model = Order
        fields = ['id', 'customer', 'status', 'datetime_created', 'items']


class OrderCreateSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cart_id):
        # try:
        #     if Cart.objects.prefetch_related('items').get(id=cart_id).items.count() == 0:
        #         raise serializers.ValidationError('Your cart is empty. Please add some products to it first!')
        # except Cart.DoesNotExist:
        #     raise serializers.ValidationError('There is no cart with this cart id!')

        if not Cart.objects.filter(id=cart_id).exists():
            raise serializers.ValidationError('There is no cart with this cart id!')

        if CartItem.objects.filter(cart_id=cart_id).count() == 0:
            raise serializers.ValidationError('Your cart is empty. Please add some products to it first!')

        return cart_id
    

    def save(self, **kwargs):
        cart_id = self.validated_data['cart_id']
        user_id = self.context['user_id']
        customer = Customer.objects.get(user_id=user_id)

        order = Order()
        order.customer = customer
        order.save()

        cart_items = CartItem.objects.select_related('product').filter(cart_id=cart_id)

        order_items = [
            OrderItem(
                order=order,
                product=cart_item.product,
                unit_price=cart_item.product.unit_price,
                quantity=cart_item.quantity,
            ) for cart_item in cart_items
        ]

        # order_items = list()
        # for cart_item in cart_items:
        #     order_item = OrderItem()
        #     order_item.order = order
        #     order_item.product_id = cart_item.product_id
        #     order_item.unit_price = cart_item.product.unit_price
        #     order_item.quantity = cart_item.quantity
            
        #     order_items.append(order_item)

        OrderItem.objects.bulk_create(order_items)

        Cart.objects.get(id=cart_id).delete()

        return order