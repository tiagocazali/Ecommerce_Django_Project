from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from .util import *
import uuid
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from datetime import datetime
from .api_mercadopago import start_payment


def homepage(request):
    
    banners = Banner.objects.all()
    context = {'banners': banners}
    return render(request, 'homepage.html', context)


def store(request, filter=None):

    product_list = filter_url(filter)
    minimum_price, maximum_price = minimum_maximum_price(product_list)
    sizes = all_sizes(product_list)

    # Apply filter from Formular 
    if request.method == 'POST': 
       
        infos = request.POST.dict()

        product_list = product_list.filter(price__gte=infos.get('minimum_price'), price__lte=infos.get('maximum_price'))
        
        if "size" in infos:
            itens = StockItem.objects.filter(quant__gt=0, product__in=product_list, size=infos.get('size'))
            products_id = itens.values_list("product", flat=True).distinct()
            product_list =product_list.filter(id__in=products_id)

        if "type" in infos:
            product_list = product_list.filter(categorytype__slug=infos.get("type"))

    #Get the Order parameter in the URL and send it to "order_itens" function. By Default is "lower-price"
    #http://127.0.0.1:8000/store/women/?order=lower-price  <== here
    order = request.GET.get("order", "lower-price")
    product_list = order_itens(product_list, order)

    context = {'products': product_list,
               'minimum_price': minimum_price,
               'maximum_price': maximum_price,
               'sizes': sizes,
            }
    
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
               'error': None
            }

    return render(request, 'checkout.html', context)


def integration_with_api(request, order_number):
    
    if request.method == 'POST':

        error =  None
        infos = request.POST.dict()

        total = float(infos.get('total'))
        order_number = Order.objects.get(id=order_number)
       
        if total != float(order_number.total_price):
            error="Invalid Price. Try again!"

        if not "address" in infos:
            error = "There is no Address for this Order!"
        
        if not request.user.is_authenticated:
            email = infos.get('email')
            try:
                validate_email(email)
            except ValidationError:
                error = "Invalid E-mail. Add a valid E-mail Address"
 
        if error:
            
            all_address = Address.objects.filter(client=order_number.client)
            context = { 'error': error,
                        'order_number': order_number,
                        'all_address': all_address,
                    }    

            return render(request, 'checkout.html', context)


        if not error:
            clients = Client.objects.filter(email=email)
            
            #Add the e-mail
            if clients:
                order_number.client = clients[0]
                order_number.client.save()
            else:
                order_number.client.email = email
                order_number.client.save()

            id_address = infos.get("address") 
            order_number.address = Address.objects.get(id=id_address)
            order_number.transaction_code = f"{order_number.id}--{datetime.now().timestamp()}"
            order_number.save()

            #Integration with Mercado Pago Payment 
            order_items = OrderItems.objects.filter(order=order_number)
            back_link = request.build_absolute_uri(reverse('payment_confirmation'))
            
            #If everything worked OK, call the function in API_MercadoPago.py
            payment_link, payment_id = start_payment(order_items, back_link) 

            #Save the Payment_id in database and return de payment Link
            payment = Payment.objects.create(payment_id=payment_id, order=order_number)
            payment.save()
            return redirect(payment_link)
    
    else:
        return redirect('store')


def payment_confirmation(request):

    infos = request.GET.dict()
    status = infos.get('status')
    preference_id = infos.get('preference_id')

    if status == 'approved':
        payment = Payment.objects.get(payment_id=preference_id)
        payment.approved = True
        payment.order.finished = True
        payment.order.purchase_date = datetime.now()
        payment.order.save() 
        payment.save()

        return redirect("payment_approved", payment.order.id)
    
    else:
        return redirect("checkout")
   

def payment_approved(request, order_id):
    order = Order.objects.get(id=order_id, finished=True)
    order_items = OrderItems.objects.filter(order=order)
    context = { 'order': order,
               'order_items': order_items 
            }
    return render(request, 'payment_approved.html', context)


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


@login_required
def profile(request):

    problem = None
    changes_done = False

    if request.method == 'POST':
        infos = request.POST.dict()
        
        # user clicked in "Change Password"
        if 'actual_password' in infos:

            actual_password = infos.get("actual_password")
            new_password = infos.get("new_password")
            confirm_password = infos.get("confirm_password")

            if new_password == confirm_password:
                user = authenticate(request, username=request.user.email, password=actual_password)
                if user:
                    user.set_password(new_password)
                    user.save()
                    changes_done = True
                
                else:
                    problem = "Wrong password! The Actual password is NOT correct. Try Again"

            else:
                problem = "New Password and Confirmation Password is NOT igual! Try again"


        # user is updating personal data - clicked in "Save"
        elif 'email' in infos:
            name = infos.get('name')
            email = infos.get('email')
            phone = infos.get('phone')

            #user changed his E-mail. Check if the new e-mail is available
            if email != request.user.email:
                search = User.objects.filter(email=email)
                if len(search) > 0:
                    problem = "E-mail already exist in Database. Try another one!"

            if not problem:
                client = request.user.client
                client.email = email
                request.user.email = email
                request.user.username = email
                client.nome = name
                client.phone = phone
                client.save()
                request.user.save()
                changes_done = True


        # user didn't fill the password neither e-mail 
        else:
            problem = "Invalid information (Form). Try again"

    
    context = {'problem': problem,
               'changes_done': changes_done,
            }
    
    return render(request, 'user/profile.html', context)


@login_required
def my_orders(request):
    client = request.user.client
    orders = Order.objects.filter(finished=True, client=client).order_by("-purchase_date")
    #falta colocar os itens de cada pedido aqui!!!
    context = {"orders": orders}
    return render(request, "user/my_orders.html", context)


def login_page(request):
    
    problem = False

    #is is already authenticated, just redirect
    if request.user.is_authenticated:
        return redirect('store')
    
    if request.method == "POST":
        infos = request.POST.dict()

        if "email" in infos and "password" in infos:
            email = infos.get("email")
            password = infos.get("password")
            user = authenticate(request, username=email, password=password)

            if user:
                login(request, user)
                return redirect('profile')
            else:
                problem = True

        else:
            problem = True
    
    context = { "problem": problem}
    return render(request, 'user/login.html', context)


def create_account(request):

    problem= None

    if request.user.is_authenticated:
        return redirect('store')
    
    if request.method == "POST":
        infos = request.POST.dict()

        if ('email' in infos) and ('password' in infos) and ('confirm_password' in infos):
            email = infos.get('email')
            password = infos.get("password")
            confirm_password = infos.get("confirm_password")

            try:
                validate_email(email)
            except ValidationError:
                problem = "Invalid email. Please enter a valid email."

            if password == confirm_password:
                #create user in USER Table, used for Django.
                user, created = User.objects.get_or_create(username=email, email=email)

                if created:
                    user.set_password(password)
                    user.save()

                    #Authenticate and make automatic login
                    user = authenticate(request, username=email, password=password)
                    login(request, user)

                    #Now create de user in the Client Table.
                    #But before create the user, check if already exist an session. If exist, just update it.
                    if request.COOKIES.get('session_id'):
                        session_id = request.COOKIES.get('session_id')
                        client = Client.objects.get(session_id=session_id)
                    else:
                        client, created = Client.objects.get_or_create(email=email)
                    
                    client.user = user
                    client.email = email
                    client.save()

                    return redirect('store')

                else:
                    problem = "User already exists. Please log in with your email."

            else:
                problem = "Invalid passwords. The confirmation must match the password."

        else:
            problem = "Incorrect input error. Use a valid e-mail and/or password"

    context = { "problem": problem}
    return render(request, 'user/create_account.html', context)


@login_required
def logout_page(request):
    logout(request)
    return redirect('login_page')


@login_required
def manage_store(request):
    if request.user.groups.filter(name="Management_Team").exists():

        finished_orders = Order.objects.filter(finished=True)
        quant_orders = len(finished_orders)
        total_invoice = sum([item.total_price for item in finished_orders]) 
        total_itens = sum([item.total_quant for item in finished_orders])

        context = {'quant_orders': quant_orders,
                   'total_invoice': total_invoice,
                   'total_itens': total_itens }
         
        return render(request, 'manage/manage_store.html', context)
        
    else:
        return redirect('store')
    

@login_required
def download_report(request, report_name):
    
    if request.user.groups.filter(name="Management_Team").exists():
        if report_name == 'orders':
            infos = Order.objects.filter(finished=True)

        elif report_name == 'client_list':
            infos = Client.objects.all()

        elif report_name == 'address_list':
            infos = Address.objects.all()
    
        return export_csv(infos) #Function in Util.py
        
    else: #User is not part of Management Team
            return redirect('store')
