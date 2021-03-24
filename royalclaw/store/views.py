from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime

from .utils import cookieCart, cartData
from .models import *


def store(request):

    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)


def cart(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print("productId: ", productId)
    print("Action: ", action)

    customer = request.user.customer
    product = Product.objects.get(id=productId)

    # create or find
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    # Logged in user
    if request.user.is_authenticated:
        customer = request.user.customer
        # create or find
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    # Guest Order
    else:
        name = data['form']['name']
        email = data['form']['email']

        cookieData = cookieCart(request)
        items = cookieData['items']

        # save to database

        # even if customer is not a user, they could still be found in the customer model
        # all orders as a guest could end up being attached to a new user
        customer, created = Customer.objects.get_or_create(email=email)
        customer.name = name
        customer.save()

        order = Order.objects.create(
            customer=customer,
            complete=False
        )

        for item in items:
            product = Product.objects.get(id=item['product']['id'])

            orderItem = OrderItem.objects.create(
                product=product,
                order=order,
                quantity=item['quantity']
            )

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    # to ensure user does not manipulate total
    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
            country=data['shipping']['country'],
        )



    return JsonResponse('Payment complete', safe=False)
