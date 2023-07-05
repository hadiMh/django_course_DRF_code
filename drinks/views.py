from django.shortcuts import render
from django.http import HttpResponse

def about_tea(request):
    return HttpResponse('I love it')

def about_coffee(request):
    return HttpResponse('I don\'t like it')
