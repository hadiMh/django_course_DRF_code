from django.shortcuts import render
from django.http import HttpResponse

def pizza(request):
    return HttpResponse('I like pizza')

def ghormesabzi(request):
    return HttpResponse('This is an Iranian food')
