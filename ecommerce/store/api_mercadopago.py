import mercadopago

public_key = "APP_USR-3d5fb284-c024-422d-8461-434c7334997c"
token = "APP_USR-1215534648379575-081808-0422dadb4f55ead8f42ac90fa05df60b-1949974391"

def start_payment(order_items, link):
    
    # Add Credentials
    sdk = mercadopago.SDK(token)

    #Create the list os Itens all itens in Dictionary Format
    items = []
    for item in order_items:
        quant = int(item.quant)
        name = item.stockitem.product.name
        price = float(item.stockitem.product.price)

        items.append(
            {
                "title": name,
                "quantity": quant,
                "unit_price": price
            }
        )


    # Cria um item na preferência
    preference_data = {
        "items": items,

        "back_urls": {
            'failure': link, 
            'pending': link, 
            'success': link
        },
    }

    preference_response = sdk.preference().create(preference_data)
    payment_link = preference_response["response"]["init_point"]
    payment_id = preference_response["response"]["id"]
    
    print(payment_link, payment_id)



