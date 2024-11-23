from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'products', views.ProductReviewViewSet, basename='product-review')
router.register(r'shops', views.ShopReviewViewSet, basename='shop-review')

app_name = 'reviews'
urlpatterns = router.urls
