from os import name
from . import views
from django.urls import path
from django.contrib.auth import views as views_django


urlpatterns = [
    path('', views.homepage, name="homepage"),
    
    path('store/', views.store, name="store"),
    path('store/<str:filter>/', views.store, name="store"),
    
    path('product/<int:product_id>/', views.product_description, name="product_description"),
    path('product/<int:product_id>/<int:color_id>/', views.product_description, name="product_description"), 
    
    path('checkout/', views.checkout, name="checkout"),
    path('cart/', views.cart, name="cart"),
    path('add-cart/<int:product_id>/', views.add_to_cart, name="add_to_cart"),
    path('remove-cart/<int:product_id>/', views.remove_to_cart, name="remove_to_cart"),
    
    path('payment-start/<int:order_number>/', views.integration_with_api, name="payment_start"),
    path('payment-confirmation/', views.payment_confirmation, name="payment_confirmation"),
    path('payment-approved/<int:order_id>/', views.payment_approved, name="payment_approved"),
    
    path('new-address/', views.new_address, name="new_address"),
    
    path('profile/', views.profile, name="profile"),
    path('my-orders/', views.my_orders, name="my_orders"),
    path('create-account/', views.create_account, name="create_account"),
    path('login-page/', views.login_page, name="login_page"),
    path('logout-page', views.logout_page, name="logout_page"),

    path('manage-store', views.manage_store, name="manage_store"),
    path('download-report/<str:report_name>/', views.download_report, name="download_report"),

    # Default Django Views - Used for Change/Reset Password
    path("password_change/", views_django.PasswordChangeView.as_view(), name="password_change"),
    path("password_change/done/", views_django.PasswordChangeDoneView.as_view(), name="password_change_done"),
    path("password_reset/", views_django.PasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", views_django.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", views_django.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", views_django.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

]