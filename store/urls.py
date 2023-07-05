from django.urls import path
from .views import say_hello

urlpatterns = [
    path('hello/', say_hello),
]

# codingyar.com/store/
# codingyar.com/store/a/bcd
# codingyar.com/store/123
# codingyar.com/store/hello/
