from django.dispatch import receiver
from store.signals import order_created

@receiver(order_created)
def after_order_created(sender, **kwargs):
    print(f'New order is created {kwargs["order"].id}')