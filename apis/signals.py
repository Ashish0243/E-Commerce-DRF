from django.db.models.signals import post_save
from django.dispatch import receiver
from cart.models import Cart, CartItem
from product.models import Product
from .models import  Order, OrderItem

@receiver(post_save,sender=Cart)
def create_order_on_checkout(sender,instance,created,**kwargs):
    if instance.checked_out and  not created:
        if not Order.objects.filter(cart=instance).exists():
            order= Order.objects.create(
                user=instance.user,
                cart=instance,
                status=Order.Status.CONFIRMED
            )
            for item in instance.items.all():
                a=  int(item.product.stock)
                Product.objects.filter(id=item.product.id).update(stock=a-item.quantity)
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity
                )
