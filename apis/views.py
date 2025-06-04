from django.http import JsonResponse
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import api_view
from rest_framework.generics import (ListAPIView, ListCreateAPIView,
                                     RetrieveAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .filters import InStockFilterBackend, ProductFilter
from .models import Product ,Category,Cart,CartItem
from .serializers import ProductSerializer ,CategorySerializer,CartSerializer,CartCreateSerializer
from rest_framework.decorators import action


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


# class OrderViewset(viewsets.ModelViewSet):
#     queryset = Order.objects.prefetch_related('items__product')
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated]
#     filterset_class = OrderFilter
#     filter_backends = [DjangoFilterBackend]

#     def get_serializer(self, *args, **kwargs):
#         kwargs['context'] = self.get_serializer_context()
#         if self.action == 'create' or self.action == 'update':
#             return OrderCreateSerializer(*args, **kwargs)
#         return super().get_serializer(*args, **kwargs)
    
#     def get_queryset(self):
#         qs= super().get_queryset()
#         if not self.request.user.is_staff:
#             qs=qs.filter(user=self.request.user)
#         return qs
    
#     @action(detail=False, methods=['get'],url_path='user-orders')
#     def user_orders(self,request):
#         order=self.get_queryset().filter(user=self.request.user)
#         serializer=self.get_serializer(order, many=True)
#         return Response(serializer.data)
    

class CategoryViewsets(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]
    filterset_class= ProductFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['price','stock']

class CartViewset(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [AllowAny]
    pagination_class=None
    
    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        if self.request.method in ['POST','PUT', 'PATCH']:
            return CartCreateSerializer(*args, **kwargs)
        return super().get_serializer(*args, **kwargs)
    
