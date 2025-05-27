from django.contrib import admin
from .models import User, Product, Order, OrderItem , Category,Cart,CartItem
admin.site.register(Category)
admin.site.register(User)
admin.site.register(Product)


class OrderItemInline(admin.TabularInline):
    model= OrderItem

class OrderAdmin(admin.ModelAdmin):
    inlines=[
        OrderItemInline
    ]

admin.site.register(Order, OrderAdmin)


class CartItemInline(admin.TabularInline):
    model = CartItem

class CartAdmin(admin.ModelAdmin):
    inlines=[CartItemInline]

admin.site.register(Cart, CartAdmin)