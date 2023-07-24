from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import F, ExpressionWrapper, DecimalField

from .models import Category, Comment, Product, Customer, OrderItem, Order

def show_data(request):
    # cat = Category.objects.create(title='Z', description='some description', top_product_id=1)

    # p1 = Product()
    # p1.name = 'p1'
    # p1.category = cat
    # p1.slug = 'p-1'
    # p1.description = 'p1 description'
    # p1.unit_price = 1000
    # p1.inventory = 1
    # p1.save()

    # p2 = Product()
    # p2.name = 'p2'
    # p2.category = cat
    # p2.slug = 'p-2'
    # p2.description = 'p2 description'
    # p2.unit_price = 2000
    # p2.inventory = 2
    # p2.save()

    # order = Order.objects.create(customer_id=1)

    # order_item1 = OrderItem.objects.create(
    #     order=order,
    #     product=p1,
    #     quantity=10,
    #     unit_price=p1.unit_price,
    # )
    # order_item2 = OrderItem.objects.create(
    #     order=order,
    #     product=p2,
    #     quantity=20,
    #     unit_price=p2.unit_price,
    # )
    # order_item3 = OrderItem.objects.create(
    #     order=order,
    #     product_id=1,
    #     quantity=30,
    #     unit_price=1000,
    # )

    # cat = Category.objects.earliest('-id')
    # cat.title = 'Q'
    # cat.save()

    OrderItem.objects.filter(order_id=31).delete()
    Order.objects.filter(id=31).delete()
    Product.objects.filter(name__in=['p1', 'p2']).delete()
    cat = Category.objects.earliest('-id')
    cat.delete()


    return render(request, 'hello.html')

