import django_filters
from .models import Product
from rest_framework import filters

    
# class OrderFilter(django_filters.FilterSet):
#     class Meta:
#         created_at = django_filters.DateFilter(field_name='created_at__date')
#         model = Order
#         fields = {
#             "status": ['exact'],
#             "created_at": ['exact', 'date', 'year', 'month', 'day','lt','gt'],
#         }

