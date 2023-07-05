from django.urls import path
from . import views

urlpatterns = [
    path('tea/', views.about_tea),
    path('coffee/', views.about_coffee),
]

