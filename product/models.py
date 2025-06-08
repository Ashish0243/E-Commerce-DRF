from django.db import models
import uuid

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
    description=models.TextField(blank=True,null=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    stock=models.PositiveIntegerField()
    image=models.ImageField(upload_to='products/',blank=True,null=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)

    @property
    def is_in_stock(self):
        return self.stock > 0
    
    @property
    def avg_rating(self):
        ratings = self.ratings.all()
        if not ratings:
            return 0
        return sum(rating.rating for rating in ratings) / len(ratings)
    
    def __str__(self):
        return self.name

