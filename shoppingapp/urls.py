from django.urls import path
from . import views


app_name = 'shoppingapp'

urlpatterns = [
    # Example:
    path('', views.index, name='index'),
    path('login/', views.loginpage, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('home/', views.home, name='home'),
    path('product/<int:product_id>/', views.product, name='product_detail'),
    path('product/<int:product_id>/reviews/', views.product_reviews, name='product_reviews'),
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart/<int:product_id>/', views.update_cart, name='update_cart'),
    path('order/', views.order, name='order'),
    path('create-razorpay-order/', views.create_razorpay_order, name='create_razorpay_order'),
    path('verify-payment/', views.verify_payment, name='verify_payment'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact")

]
