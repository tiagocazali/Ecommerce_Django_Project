from django.shortcuts import render
from .models import *


def homepage(request):
    banners = Banner.objects.all()
    context = {'banners': banners}
    return render(request, 'homepage.html', context)


def store(request, category=None):
    product_list = Product.objects.filter(active=True)
    if category:
        product_list = product_list.filter(categorytype_id__name=category)
    context = {'products': product_list}
    return render(request, 'store.html', context)


def product_description(request, product_id):
    product = Product.objects.get(id=product_id)
    context = {'product': product}
    return render(request, 'product_description.html', context)


def shopping_cart(request):
    return render(request, 'shopping_cart.html')


def checkout(request):
    return render(request, 'checkout.html')


def profile(request):
    return render(request, 'profile.html')


def login(request):
    return render(request, 'login.html')

