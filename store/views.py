from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import F, ExpressionWrapper, DecimalField

from .models import Comment, Product, Customer, OrderItem, Order

def show_data(request):
    # way 1
    Comment.objects.create(
        name='hadi',
        body='Django is gread. I Love IT!',
        product_id=1,
    )

    # way 2
    product = Product.objects.get(id=1)

    new_comment = Comment()
    new_comment.name = 'HADI'
    new_comment.body = 'I LOVE to learn DJANGO!'
    new_comment.product = product
    new_comment.save()

    return render(request, 'hello.html')

