from django.http import JsonResponse
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .filters import OrderFilter
from .models import Order
from .serializers import OrderSerializer


class OrderViewset(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = OrderFilter
    filter_backends = [DjangoFilterBackend]
    
    def get_queryset(self):
        qs= super().get_queryset()
        if not self.request.user.is_staff:
            qs=qs.filter(user=self.request.user)
        return qs
    
    def get_permissions(self):
        if self.request.method not in ['GET',]:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
    
#     @action(detail=False, methods=['get'],url_path='user-orders')
#     def user_orders(self,request):
#         order=self.get_queryset().filter(user=self.request.user)
#         serializer=self.get_serializer(order, many=True)
#         return Response(serializer.data)
    


