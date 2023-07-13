from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500, blank=True)


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    slug = models.SlugField()
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)


class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)


class Order(models.Model):
    ORDER_STATUS_PAID = 'p'
    ORDER_STATUS_UNPAID = 'u'
    ORDER_STATUS_CANCELED = 'c'
    ORDER_STATUS = [
        (ORDER_STATUS_PAID,'Paid'),
        (ORDER_STATUS_UNPAID,'Unpaid'),
        (ORDER_STATUS_CANCELED,'Canceled'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    datetime_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=ORDER_STATUS, default=ORDER_STATUS_UNPAID)


class Comment(models.Model):
    COMMENT_STATUS_WAITING = 'w'
    COMMENT_STATUS_APPROVED = 'a'
    COMMENT_STATUS_NOT_APPROVED = 'na'
    COMMENT_STATUS = [
        (COMMENT_STATUS_WAITING, 'Waiting'),
        (COMMENT_STATUS_APPROVED, 'Approved'),
        (COMMENT_STATUS_NOT_APPROVED, 'Not Approved'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    body = models.TextField()
    datetime_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=2, choices=COMMENT_STATUS, default=COMMENT_STATUS_WAITING)
