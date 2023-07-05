from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome_message),
    path('hello/', views.say_hello),
    path('bye/', views.say_bye),
    path('123/', views.say_123),
    path('something/<int:num>/', views.something),
]
