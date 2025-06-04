from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
class User(AbstractUser):
    phone_number=models.CharField(max_length=15)
    email=models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Category(models.Model):
    cat_id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    category_name=models.CharField(max_length=100,unique=True)
    slug=models.CharField(max_length=100,unique=True)
    description=models.TextField(blank=True,null=True)
    image=models.ImageField(upload_to='categories/',blank=True,null=True)

    class Meta:
        verbose_name='Category'
        verbose_name_plural='Categories'

    def __str__(self):
        return self.category_name

class Product(models.Model):
    name=models.CharField(max_length=200)
    description=models.TextField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    stock=models.PositiveIntegerField()
    image=models.ImageField(upload_to='products/',blank=True,null=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)

    @property
    def is_in_stock(self):
        return self.stock > 0
    
    def __str__(self):
        return self.name
    
class Order(models.Model):
    class Status(models.TextChoices):
        PENDING='Pending' 
        CONFIRMED='Confirmed'
        CANCELLED='Cancelled'
    
    order_id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    cart=models.ForeignKey('Cart', on_delete=models.CASCADE ,null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=20,choices=Status.choices,default=Status.PENDING) 
    products=models.ManyToManyField(Product,through='OrderItem',related_name='orders') 

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
