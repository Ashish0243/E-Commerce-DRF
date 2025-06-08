from django.shortcuts import render
from .models import Product,Category
from .serializers import ProductSerializer,CategorySerializer,ProductListSerializer
from .filters import InStockFilterBackend,ProductFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework import viewsets

class CategoryViewsets(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['category_name']
    search_fields = ['category_name','description']

class ProductViewsets(viewsets.ModelViewSet):
    queryset= Product.objects.all()
    serializer_class=ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter, InStockFilterBackend]
    filterset_class = ProductFilter
    ordering_fields = ['name', 'price','stock']
    search_fields = ['name', 'description','price']
    
    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()
    
    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        if self.request.method in ['GET']:
            return ProductListSerializer(*args, **kwargs)
        return super().get_serializer(*args, **kwargs)