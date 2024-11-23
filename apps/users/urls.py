from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('register/', views.UserRegistrationView.as_view(), name='user-registration'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
]