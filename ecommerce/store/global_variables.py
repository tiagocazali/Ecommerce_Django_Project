from .models import Order, OrderItems, Client, Category, CategoryType


def quant_cart_itens (request):
    
    quant_cart_itens = 0
    
    if request.user.is_authenticated:
        client = request.user.client

    else:
        # User is NOT authenticated, but already have a active session, get it
        if request.COOKIES.get('session_id'):
            session_id = request.COOKIES.get('session_id')
            client, created = Client.objects.get_or_create(session_id=session_id)
        
        # User doesn't exist. Cart is empty
        else:
            return {'quant_cart_itens': quant_cart_itens}
    
    order_number, created = Order.objects.get_or_create(client_id = client.id, finished=False)
    order_itens = OrderItems.objects.filter(order_id = order_number)
    
    for each_item in order_itens:
        quant_cart_itens += each_item.quant
    
    return {'quant_cart_itens': quant_cart_itens}


def all_category_und_type(request):
    
    all_category = Category.objects.all()
    all_type = CategoryType.objects.all()

    return { 'all_category':all_category, 'all_type':all_type}


def management_team(request):
    is_management_team = False
    if request.user.is_authenticated: 
        if request.user.groups.filter(name="Management_Team").exists():
            is_management_team = True
    
    return {'is_management_team': is_management_team}
