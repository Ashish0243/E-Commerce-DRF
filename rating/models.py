from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Rating(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE, related_name='ratings')
    product= models.ForeignKey('product.Product', on_delete=models.CASCADE, related_name='ratings')
    rating=models.PositiveIntegerField()
    review=models.TextField(blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} rated {self.product.name} with {self.rating} stars'