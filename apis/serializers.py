from .models import User, Order
from cart.models import CartItem
from rest_framework import serializers
from django.db import transaction
from dj_rest_auth.registration.serializers import RegisterSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('id','username','email')


class CustomRegisterSerializer(RegisterSerializer):
    first_name=serializers.CharField(required=True)
    last_name=serializers.CharField(required=False,allow_blank=True)
    phone_number=serializers.CharField(required=True, allow_blank=False)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['first_name'] = self.validated_data.get('first_name', '')
        data['last_name'] = self.validated_data.get('last_name', '')
        data['phone_number'] = self.validated_data.get('phone_number', '')
        return data
    def save(self, request):
        user = super().save(request)
        user.first_name = self.validated_data.get('first_name', '')
        user.last_name = self.validated_data.get('last_name', '')
        user.phone_number = self.validated_data.get('phone_number', '')
        user.save()
        return user

class OrderSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    id= serializers.UUIDField(source='order_id', read_only=True)
    class CartItemCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model=CartItem
            fields=('product','quantity')
    items=CartItemCreateSerializer(many=True)
    class Meta:
        model = Order
        fields = ('id', 'user', 'cart','status', 'created_at','items','total_amount')
        extra_kwargs = {
            'user': {'read_only': True},
            'id':{'read_only': True},
            'created_at': {'read_only': True},
    
        }
