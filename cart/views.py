from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Cart
from .serializers import CartSerializer, CartCreateSerializer
# Create your views here.
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
    
