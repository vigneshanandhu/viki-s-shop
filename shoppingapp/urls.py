from django.urls import path
from . import views


app_name = 'shoppingapp'

urlpatterns = [
    # Example:
    path('', views.index, name='index'),
    path('login/', views.loginpage, name='login'),
    path('register/', views.register, name='register'),
    path('home/', views.home, name='home'),
]