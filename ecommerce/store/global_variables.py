from .models import Order, OrderItems


def quant_cart_itens (request):
    
    quant_cart_itens = 0
    
    if request.user.is_authenticated:
        client = request.user.client
    else:
        return {'quant_cart_itens': quant_cart_itens}
    
    order_number, created = Order.objects.get_or_create(client_id = client, finished=False)
    order_itens = OrderItems.objects.filter(order_id = order_number)
    for each_item in order_itens:
        quant_cart_itens += each_item.quant
    
    return {'quant_cart_itens': quant_cart_itens}