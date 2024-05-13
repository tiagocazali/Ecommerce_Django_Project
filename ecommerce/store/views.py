from django.shortcuts import render, redirect
from .models import *
import uuid


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
    selected_color = None
    
    product = Product.objects.get(id=product_id)
    product_in_stock = StockItem.objects.filter(product_id=product, quant__gt=0)
    
    if len(product_in_stock) > 0:
        in_stock = True
        colors = {each.color for each in product_in_stock}

        if color_id:
            selected_color = Color.objects.get(id=color_id)
            product_in_stock = StockItem.objects.filter(product_id=product, quant__gt=0, color__id=color_id)
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

        # If user IS Authenticated, get it. 
        if request.user.is_authenticated:
            client = request.user.client

        else: 
            # User is NOT authenticated, but already have a active session, get it
            if request.COOKIES.get('session_id'):
                session_id = request.COOKIES.get('session_id')
                client = Client.objects.get(session_id=session_id)

            # If it is a NEW user, create an anonymous session for him 
            else:
                session_id = str(uuid.uuid4())
                resposta.set_cookie(key='session_id', value=session_id, max_age=60*60*24*30) #Total of 30 days in Seconds
                
            client, created = Client.objects.get_or_create(session_id=session_id)

        order, created = Order.objects.get_or_create(client_id=client, finished=False)
        stockItem = StockItem.objects.get(product_id__id=product_id, color__id=color_id, size=size)
        order_items, created = OrderItems.objects.get_or_create(order_id=order, stockitem_id=stockItem)
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
        
        if request.user.is_authenticated:
            client = request.user.client

        else:
            # User is NOT authenticated, but already have a active session, get it
            if request.COOKIES.get('session_id'):
                session_id = request.COOKIES.get('session_id')
                client, created = Client.objects.get_or_create(session_id=session_id)
        
            # User doesn't exist. Cart is empty
            else:
                return redirect('store')
            
        order, created = Order.objects.get_or_create(client_id=client, finished=False)
        stockItem = StockItem.objects.get(product_id__id=product_id, color__id=color_id, size=size)

        order_items, created = OrderItems.objects.get_or_create(order_id=order, stockitem_id=stockItem)
        order_items.quant -= 1
        order_items.save()
        
        if order_items.quant <= 0:
            order_items.delete()

        return redirect('cart')
    
    else:
        return redirect('store')


def cart(request):
    
    if request.user.is_authenticated:
        client = request.user.client
            
    else: 
        # User is NOT authenticated, but already have a active session, get it
        if request.COOKIES.get('session_id'):
            session_id = request.COOKIES.get('session_id')
            client, created = Client.objects.get_or_create(session_id=session_id)
        
        # User doesn't exist. Cart is empty
        else:
            context = {'user_exist': False,}
            return render(request, 'shopping_cart.html', context)


    order_number, created = Order.objects.get_or_create(client_id = client, finished=False)
    order_itens = OrderItems.objects.filter(order_id = order_number)
    
    context = {'user_exist': True,
               'order_itens': order_itens,
               'order_number': order_number,
            }
    
    return render(request, 'shopping_cart.html', context)


def checkout(request):

    if request.user.is_authenticated:
        client = request.user.client
            
    else: 
        # User is NOT authenticated, but already have a active session, get it
        if request.COOKIES.get('session_id'):
            session_id = request.COOKIES.get('session_id')
            client, created = Client.objects.get_or_create(session_id=session_id)
        
        # User doesn't exist. Cart is empty
        else:
            return redirect('store')

    order_number = Order.objects.get(client_id = client, finished=False)
    all_address = Address.objects.filter(client_id=client)
        
    context = {'order_number': order_number,
               'all_address': all_address,
            }

    return render(request, 'checkout.html', context)


def new_address(request):
    
    if request.user.is_authenticated:
        client = request.user.client
            
    else: 
        # User is NOT authenticated, but already have a active session, get it
        if request.COOKIES.get('session_id'):
            session_id = request.COOKIES.get('session_id')
            client = Client.objects.get(session_id=session_id)
        
        # User doesn't exist. Cart is empty
        else:
            return redirect('store')
        
    # User SEND (add) a new Address        
    if request.method == "POST": 
        infos = request.POST.dict()
        address = Address.objects.create(client_id=client,
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
        all_address = Address.objects.filter(client_id=client)
        
        context = {'all_address': all_address,}
        return render(request, 'new_address.html', context)


def profile(request):
    return render(request, 'profile.html')


def login(request):
    return render(request, 'login.html')


# TODO: TEM QUE CRIAR A TELA DE CADASTRO DE USUÁRIO