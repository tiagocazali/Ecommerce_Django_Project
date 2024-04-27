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


def product_description(request, product_id, color_id=None):
    in_stock = False
    sizes = {}
    colors = {}
    selected_color_name = None
    
    product = Product.objects.get(id=product_id)
    product_in_stock = StockItem.objects.filter(product_id=product, quant__gt=0)
    
    if len(product_in_stock) > 0:
        in_stock = True
        colors = {each.color for each in product_in_stock}

        if color_id:
            selected_color_name = (Color.objects.get(id=color_id)).name
            product_in_stock = StockItem.objects.filter(product_id=product, quant__gt=0, color__id=color_id)
            sizes = {each.size for each in product_in_stock}

    context = {'product': product, 
               'stock_itens': product_in_stock, 
               'in_stock': in_stock, 
               'colors': colors, 
               'sizes': sizes,
               'selected_color_name': selected_color_name,
            }
    
    return render(request, 'product_description.html', context)


def shopping_cart(request):
    return render(request, 'shopping_cart.html')


def checkout(request):
    return render(request, 'checkout.html')


def profile(request):
    return render(request, 'profile.html')


def login(request):
    return render(request, 'login.html')

