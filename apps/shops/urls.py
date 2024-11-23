from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.ShopViewSet, basename='shop')

app_name = 'shops'
urlpatterns = router.urls