from .models import Product, Client, StockItem
from django.db.models import Min, Max


def get_user_id(request):
    """Function to Get user_id if the user IS or NOT Authenticated"""

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


def filter_url(filter):

    product_list = []

    if filter: 
        if "-" in filter:
            # Filter contain: "category-type"
            category, category_type = filter.split("-")
            product_list = Product.objects.filter(category__slug=category, categorytype__slug=category_type, active=True)
        
        else:
            #Filter contain only "category"
            product_list = Product.objects.filter(category__slug=filter, active=True)
    
    else:
        #there is no filter, so show all products
        product_list = Product.objects.filter(active=True)
    
    return product_list


def minimum_maximum_price(product_list):

    minimum_price= 0
    maximum_price = 0

    if len(product_list) > 0: 
        minimum_price = list(product_list.aggregate(Min("price")).values())[0]
        minimum_price = round(minimum_price, 2)

        maximum_price = list(product_list.aggregate(Max("price")).values())[0]
        maximum_price = round(maximum_price, 2)

    return minimum_price, maximum_price


def all_sizes(product_list):
    
    itens = StockItem.objects.filter(quant__gt=0, product__in=product_list)
    sizes = itens.values_list("size", flat=True).distinct()

    return sizes


def order_itens(product_list, order):

    if order == "lower-price":
        product_list = product_list.order_by('price')
    
    elif order == "higher-price":
        product_list = product_list.order_by('-price')
    
    elif order == "most-popular":
        aux_list = []
        for product in product_list:
            aux_list.append((product.total_sell(), product))

        aux_list = sorted(aux_list, key=lambda x: x[0], reverse=True)
        product_list = [item[1] for item in aux_list]

    return product_list