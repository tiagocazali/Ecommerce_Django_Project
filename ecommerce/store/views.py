from django.shortcuts import render, redirect
from .models import *
import uuid


def get_user_id(request):
    """Function to Get user_id if the user is or not Authenticated"""

    if request.user.is_authenticated:
            client = request.user.client

    else:
        # User is NOT authenticated, but already have a active session, get it
        if request.COOKIES.get('session_id'):
            session_id = request.COOKIES.get('session_id')
            client = Client.objects.get(session_id=session_id)
    
        # User doesn't exist. Cart is empty
        else:
            client=None
    
    return client


def homepage(request):
    
    banners = Banner.objects.all()
    context = {'banners': banners}
    return render(request, 'homepage.html', context)


def store(request, category=None):

    product_list = Product.objects.filter(active=True)

    if category:
        product_list = product_list.filter(category__slug=category)

    context = {'products': product_list}
    return render(request, 'store.html', context)


def product_description(request, product_id, color_id=None):
    
    in_stock = False
    sizes = {}
    colors = {}
    selected_color = None
    
    product = Product.objects.get(id=product_id)
    product_in_stock = StockItem.objects.filter(product=product, quant__gt=0)
    
    if len(product_in_stock) > 0:
        in_stock = True
        colors = {each.color for each in product_in_stock}

        if color_id:
            selected_color = Color.objects.get(id=color_id)
            product_in_stock = StockItem.objects.filter(product=product, quant__gt=0, color__id=color_id)
            sizes = {each.size for each in product_in_stock}

    context = {'product': product, 
               'in_stock': in_stock, 
               'colors': colors, 
               'sizes': sizes,
               'selected_color': selected_color,
            }
    
    return render(request, 'product_description.html', context)


def add_to_cart(request, product_id):

    if request.method == 'POST' and product_id:
        
        infos = request.POST.dict()
        color_id = infos.get('color')
        size = infos.get('size')

        resposta = redirect('cart')

        client = get_user_id(request)

        # If it is a NEW user, create an anonymous session for him 
        if not client:
            session_id = str(uuid.uuid4())
            resposta.set_cookie(key='session_id', value=session_id, max_age=60*60*24*30) #Total of 30 days in Seconds
            client, created = Client.objects.get_or_create(session_id=session_id)

        order, created = Order.objects.get_or_create(client=client, finished=False)
        stockItem = StockItem.objects.get(product__id=product_id, color__id=color_id, size=size)
        order_items, created = OrderItems.objects.get_or_create(order=order, stockitem=stockItem)
        order_items.quant += 1
        order_items.save()

        return resposta
    
    else:
        return redirect('store')


def remove_to_cart(request, product_id):
    
    if request.method == 'POST' and product_id:
        
        infos = request.POST.dict()
        color_id = infos.get('color')
        size = infos.get('size')
        
        client= get_user_id(request)
    
        # User doesn't exist. Cart is empty
        if not client:
            return redirect('store')
            
        order, created = Order.objects.get_or_create(client=client, finished=False)
        stockItem = StockItem.objects.get(product__id=product_id, color__id=color_id, size=size)

        order_items, created = OrderItems.objects.get_or_create(order=order, stockitem=stockItem)
        order_items.quant -= 1
        order_items.save()
        
        if order_items.quant <= 0:
            order_items.delete()

        return redirect('cart')
    
    else:
        return redirect('store')


def cart(request):
    
    client = get_user_id(request)

    # User doesn't exist. Cart is empty
    if not client:
        context = {'user_exist': False,}
        return render(request, 'shopping_cart.html', context)

    order_number, created = Order.objects.get_or_create(client = client, finished=False)
    order_itens = OrderItems.objects.filter(order_id = order_number)
    
    context = {'user_exist': True,
               'order_itens': order_itens,
               'order_number': order_number,
            }
    
    return render(request, 'shopping_cart.html', context)


def checkout(request):

    client = get_user_id(request)

    # User doesn't exist. Cart is empty
    if not client:
        return redirect('store')

    order_number = Order.objects.get(client = client, finished=False)
    all_address = Address.objects.filter(client=client)
        
    context = {'order_number': order_number,
               'all_address': all_address,
            }

    return render(request, 'checkout.html', context)


def new_address(request):
    
    client = get_user_id(request)

    # User SEND (add) a new Address        
    if request.method == "POST": 
        infos = request.POST.dict()
        address = Address.objects.create(client=client,
                                         description=infos.get('description'),
                                         street=infos.get('street'),
                                         number=int(infos.get('number')),
                                         complement=infos.get('complement'),
                                         cep=infos.get('cep'),
                                         city=infos.get('city'),
                                         state=infos.get('state'),
                                         country=infos.get('country'),
                                        )
        address.save()
        return redirect('checkout')

    # User GET the existing data
    else:
        all_address = Address.objects.filter(client=client)
        
        context = {'all_address': all_address,}
        return render(request, 'new_address.html', context)


def profile(request):
    return render(request, 'profile.html')


def login(request):
    return render(request, 'login.html')


# TODO: TEM QUE CRIAR A TELA DE CADASTRO DE USUÁRIO