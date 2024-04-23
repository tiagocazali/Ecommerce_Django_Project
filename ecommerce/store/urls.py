from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('store/', views.store, name="store"),
    path('shopping_cart/', views.shopping_cart, name="shopping_cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('profile/', views.profile, name="profile"),
    path('login/', views.login, name="login"),
]