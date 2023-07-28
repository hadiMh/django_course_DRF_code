from django.urls import path, include
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register('products', views.ProductViewSet, basename='product')
router.register('categories', views.CategoryViewSet, basename='category')

urlpatterns = router.urls

# urlpatterns = [
#     path('', include(router.urls)),
# ]

# urlpatterns = [
#     path('products/', views.ProductList.as_view()),
#     path('products/<int:pk>/', views.ProductDetail.as_view()),
#     path('categories/', views.CategoryList.as_view()),
#     path('categories/<int:pk>/', views.CategoryDetail.as_view(), name='category-detail'),
# ]
