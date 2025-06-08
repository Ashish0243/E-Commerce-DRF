import django_filters
from .models import Product
from rest_framework import filters

class InStockFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(stock__gt=0)
    
class ProductFilter(django_filters.FilterSet):
    category_slug= django_filters.CharFilter(field_name='category__slug')
    class Meta:
        model = Product
        fields={
            'price':['exact', 'lt', 'lte', 'gt', 'gte', 'range'],
            'name':['exact', 'icontains']
        }
      