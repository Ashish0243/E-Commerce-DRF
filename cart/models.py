
import uuid
from django.db import models
from product.models import Product,Category
from django.contrib.auth import get_user_model
User=get_user_model()

class Cart(models.Model):
    cart_id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    date_added=models.DateTimeField(auto_now_add=True)
    checked_out=models.BooleanField(default=False)
    products=models.ManyToManyField(Product, through='CartItem', related_name='carts')

    def __str__(self):
        return f'Cart {self.cart_id} for {self.user.username}'
    
class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='items')
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} x {self.product.name} in Cart {self.cart.cart_id}'