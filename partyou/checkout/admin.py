from django.contrib import admin

from partyou.checkout.models import CartItem, Order, OrderItem


admin.site.register([CartItem, Order, OrderItem])
