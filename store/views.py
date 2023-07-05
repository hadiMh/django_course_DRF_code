from django.shortcuts import render
from django.http import HttpResponse

def say_hello(request):
    # ...
    return HttpResponse('Hello World!')

def say_bye(request):
    return HttpResponse('Goodbye')

def say_123(request):
    return HttpResponse('This is the number of 123')

def welcome_message(request):
    return HttpResponse('Welcome to the store')

def something(request, num):
    print(num)
    print(type(num))
    return HttpResponse('something')
