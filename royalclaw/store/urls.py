from django.urls import path
from . import views


urlpatterns = [
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),

    # need all three so that you can update from store, cart, and checkout
    path('update_item/', views.updateItem, name="update_item"),
    path('cart/update_item/', views.updateItem, name="update_item"),
    path('checkout/update_item/', views.updateItem, name="update_item"),

    # submitting an order
    path('process_order/', views.processOrder, name="process_order"),
    path('checkout/process_order/', views.processOrder, name="process_order"),
]