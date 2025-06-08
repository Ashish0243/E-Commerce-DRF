from django.contrib import admin
from .models import User, Order, OrderItem 
admin.site.register(User)
class OrderItemInline(admin.TabularInline):
    model= OrderItem

class OrderAdmin(admin.ModelAdmin):
    inlines=[
        OrderItemInline
    ]

admin.site.register(Order, OrderAdmin)


