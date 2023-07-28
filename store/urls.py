from django.urls import path, include
from rest_framework.routers import SimpleRouter, DefaultRouter

from . import views

router = DefaultRouter()
router.register('products', views.ProductViewSet, basename='product')
router.register('categories', views.CategoryViewSet, basename='category')

urlpatterns = router.urls
