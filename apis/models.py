from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from product.models import Product, Category
class User(AbstractUser):
    phone_number=models.CharField(max_length=15)
    email=models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
class Order(models.Model):
    class Status(models.TextChoices):
        PENDING='Pending' 
        CONFIRMED='Confirmed'
        CANCELLED='Cancelled'
    
    order_id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    cart=models.ForeignKey('cart.Cart', on_delete=models.CASCADE ,null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=20,choices=Status.choices,default=Status.PENDING) 
    products=models.ManyToManyField(Product,through='OrderItem',related_name='orders') 
    
    @property
    def total_amount(self):
        return sum(item.subtotal for item in self.items.all())
    def __str__(self):
        return f'Order {self.order_id} by {self.user.username}' 


class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()
    
    @property
    def subtotal(self):
        return self.product.price*self.quantity
    
    def __str__(self):
        return f'{self.quantity} x {self.product.name} in {self.order.order_id}'
      

