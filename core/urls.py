# core/urls.py
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/test-connection/', views.test_connection, name='test-connection'),
    path('api/cart/', include('apps.cart.urls')),
    path('api/orders/', include('apps.orders.urls')),
    path('api/products/', include('apps.products.urls')),
    path('api/reviews/', include('apps.reviews_ratings.urls')),
    path('api/shops/', include('apps.shops.urls')),
    path('api/users/', include('apps.users.urls')),
    path('api/wishlist/', include('apps.wishlist.urls')),
]