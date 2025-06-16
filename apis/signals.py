from django.db.models.signals import post_save
from django.dispatch import receiver
from cart.models import Cart, CartItem
from product.models import Product
from .models import  Order, OrderItem
from .tasks import send_email_task
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

@receiver(post_save, sender=Order)
def send_email_on_order_creation(sender, instance, created, **kwargs):
    if created:
        res=send_email_task.delay(instance.user.email,str(instance.order_id))
        print(res.result)