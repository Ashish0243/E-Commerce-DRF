import django_filters
from .models import Product
from rest_framework import filters

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            "name":['exact', 'icontains'],
            "price": ['exact', 'lt', 'lte',
                      'gt', 'gte','range'],
        }

class InStockFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(stock__gt=0)
    
# class OrderFilter(django_filters.FilterSet):
#     class Meta:
#         created_at = django_filters.DateFilter(field_name='created_at__date')
#         model = Order
#         fields = {
#             "status": ['exact'],
#             "created_at": ['exact', 'date', 'year', 'month', 'day','lt','gt'],
#         }

class ProductFilter(django_filters.FilterSet):
    category_slug= django_filters.CharFilter(field_name='category__slug')
    class Meta:
        model = Product
        fields={
            'price':['exact', 'lt', 'lte', 'gt', 'gte', 'range'],
            'name':['exact', 'icontains']
        }
      