from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('store/', views.store, name="store"),
    path('store/<str:category>/', views.store, name="store"),
    path('checkout/', views.checkout, name="checkout"),
    path('profile/', views.profile, name="profile"),
    path('login/', views.login, name="login"),
    path('product/<int:product_id>/', views.product_description, name="product_description"),
    path('product/<int:product_id>/<int:color_id>/', views.product_description, name="product_description"), 
    path('my-cart/<int:product_id>/', views.add_to_cart, name="add_to_cart"),
    path('cart/', views.cart, name="cart"),
]