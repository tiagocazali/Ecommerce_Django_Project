from django.shortcuts import render
from .models import *

# Create your views here.
def homepage(request):
    return render(request, 'homepage.html')

def store(request):
    product_list = Product.objects.all()
    context = {'products': product_list}
    return render(request, 'store.html', context)

def shopping_cart(request):
    return render(request, 'shopping_cart.html')

def checkout(request):
    return render(request, 'checkout.html')

def profile(request):
    return render(request, 'profile.html')

def login(request):
    return render(request, 'login.html')

