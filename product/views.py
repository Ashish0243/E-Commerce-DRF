from django.shortcuts import render
from .models import Product,Category
from .serializers import ProductSerializer,CategorySerializer
from .filters import InStockFilterBackend, ProductFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import (ListAPIView, ListCreateAPIView,
                                         RetrieveAPIView,
                                         RetrieveUpdateDestroyAPIView)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework import viewsets


class ProductListCreateView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends=[DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter,InStockFilterBackend]
    ordering_fields = ['name', 'price']
    serach_fields = ['name','description']
    pagination_class= LimitOffsetPagination
    def get_permissions(self):
        self.permission_classes=[AllowAny]
        if self.request.method == 'POST':
            self.permission_classes= [IsAdminUser]
        return super().get_permissions()

class ProductDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        self.permission_classes=[AllowAny]
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes= [IsAdminUser]
        return super().get_permissions()

class CategoryViewsets(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]
    filterset_class= ProductFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['price','stock']