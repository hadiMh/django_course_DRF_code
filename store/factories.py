import random
import factory
from datetime import datetime
from faker import Faker
from factory.django import DjangoModelFactory

from . import models

faker = Faker()

class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = models.Category

    title = factory.Faker(
        "sentence",
        nb_words=5,
        variable_nb_words=True
    )
    description = factory.Faker('paragraph', nb_sentences=1, variable_nb_sentences=False)


class DiscountFactory(DjangoModelFactory):
    class Meta:
        model = models.Discount

    discount = factory.LazyFunction(lambda: random.randint(1, 80)/100)
    description = factory.Faker('paragraph', nb_sentences=1, variable_nb_sentences=False)


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = models.Product

    name = factory.LazyAttribute(lambda x: ' '.join([x.capitalize() for x in faker.words(3)]))
    slug = factory.LazyAttribute(lambda x: '-'.join(x.name.split(' ')).lower())
    description = factory.Faker('paragraph', nb_sentences=5, variable_nb_sentences=True)
    unit_price = factory.LazyFunction(lambda: random.randint(1, 1000) + random.randint(0, 100)/100)
    inventory = factory.LazyFunction(lambda: random.randint(1, 100))


class CustomerFactory(DjangoModelFactory):
    class Meta:
        model = models.Customer

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    phone_number = factory.Faker("phone_number")
    birth_date = factory.LazyFunction(lambda: faker.date_time_ad(start_datetime=datetime(1990,1,1), end_datetime=datetime(2015,1,1)))


class AddressFactory(DjangoModelFactory):
    class Meta:
        model = models.Address

    province = factory.Faker("word")
    city = factory.Faker("word")
    street = factory.LazyFunction(lambda: f'street {random.randint(1, 50)}')


class OrderFactory(DjangoModelFactory):
    class Meta:
        model = models.Order

    status = factory.LazyFunction(lambda: random.choice([models.Order.ORDER_STATUS_UNPAID, models.Order.ORDER_STATUS_CANCELED]))


class OrderItemFactory(DjangoModelFactory):
    class Meta:
        model = models.OrderItem

    quantity = factory.LazyFunction(lambda: random.randint(1, 20))


class CommentFactory(DjangoModelFactory):
    class Meta:
        model = models.Comment

    name = factory.Faker("first_name")
    body = factory.Faker('paragraph', nb_sentences=3, variable_nb_sentences=True)
    status = factory.LazyFunction(lambda: random.choice([models.Comment.COMMENT_STATUS_WAITING, models.Comment.COMMENT_STATUS_APPROVED, models.Comment.COMMENT_STATUS_NOT_APPROVED]))


class CartFactory(DjangoModelFactory):
    class Meta:
        model = models.Cart


class CartItemFactory(DjangoModelFactory):
    class Meta:
        model = models.CartItem

    quantity = factory.LazyFunction(lambda: random.randint(1, 20))
    


