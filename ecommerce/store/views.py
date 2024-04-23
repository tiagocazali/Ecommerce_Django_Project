from django.shortcuts import render

# Create your views here.
def homepage(request):
    return render(request, 'homepage.html')

def store(request):
    return render(request, 'store.html')

def shopping_cart(request):
    return render(request, 'shopping_cart.html')

def checkout(request):
    return render(request, 'checkout.html')

def profile(request):
    return render(request, 'profile.html')

def login(request):
    return render(request, 'login.html')

