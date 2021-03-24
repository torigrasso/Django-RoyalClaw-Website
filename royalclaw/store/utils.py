import json
from .models import *


def cookieCart(request):
    # get cart cookie
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        # first time on web page cart might not exist
        cart = {}

    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    cartItems = order['get_cart_items']

    # keeps user from seeing error (example: if cart has a product that doesn't exist anymore)
    # need to find a way to remove it from cookie cart
    try:
        # update cart
        for i in cart:
            cartItems += cart[i]['quantity']

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL
                },
                'quantity': cart[i]['quantity'],
                'get_total': total
            }
            items.append(item)

            if product.digital == False:
                order['shipping'] = True
    except:
        pass

    return {'cartItems':cartItems, 'order':order, 'items':items}


def cartData(request):
    # Logged in user
    if request.user.is_authenticated:
        customer = request.user.customer
        # create or find
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    # User that is not logged in
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    return {'cartItems':cartItems, 'order':order, 'items':items}


