from .models import Product, Order, OrderItem,User, Category ,Cart, CartItem
from rest_framework import serializers
from django.db import transaction
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=('cat_id','category_name','slug','description')
        extra_kwargs = {
            'slug': {'read_only': True},
            'cat_id': {'read_only': True}
        }

    def create(self, validated_data):
        slug_data= validated_data.get('category_name')
        validated_data['slug'] = slug_data.lower().replace(' ', '-')
        slug=Category.objects.create(**validated_data)
        return slug
    
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model= Product
        fields=('name','description','price','stock','category')
    
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('id','username','email')

class OrderItemSerializer(serializers.ModelSerializer):
    product_name=serializers.CharField(source='product.name')
    product_price=serializers.DecimalField(source='product.price',max_digits=10,decimal_places=2)
    class Meta:
        model=OrderItem
        fields=('product_name','product_price','quantity')


class OrderSerializer(serializers.ModelSerializer):
    order_id=serializers.UUIDField(read_only=True)
    items=OrderItemSerializer(many=True)
    total_price=serializers.SerializerMethodField()
    def get_total_price(self,obj):
        print(obj.items.all())
        return sum(item.subtotal for item in obj.items.all())

    class Meta:
        model= Order
        fields=('order_id','user','created_at','status','items','total_price')

class OrderCreateSerializer(serializers.ModelSerializer):
    class OrderItemCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model=OrderItem
            fields=('product','quantity')
    items=OrderItemCreateSerializer(many=True)
    order_id=serializers.UUIDField(read_only=True)

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)
    def update(self, instance, validated_data):
        items_data = validated_data.pop('items')
        with transaction.atomic():
            instance=super().update(instance, validated_data)

            if items_data is not None:
                instance.items.all().delete()
                for item in items_data:
                    OrderItem.objects.create(order=instance, **item)
        return instance

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user=self.context['request'].user
        with transaction.atomic():
            order = Order.objects.create(user=user,**validated_data)

            for items in items_data:
                OrderItem.objects.create(order=order,**items)

        return order


    class Meta:
        model=Order
        fields=(
            'user',
            'order_id',
            'status',
            'items'
        )
        extra_kwargs={
            "user" : {"read_only": True}
        }




class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    class Meta:
        model=CartItem
        fields=('product_name','product_price','quantity')

class CartSerializer(serializers.ModelSerializer):
    items=CartItemSerializer(many=True)
    class Meta:
        model=Cart
        fields=('cart_id','user','date_added','checked_out','items')
        extra_kwargs = {
            'cart_id': {'read_only': True},
            'date_added': {'read_only': True}
        }

class CartCreateSerializer(serializers.ModelSerializer):
    cart_id=serializers.UUIDField(read_only=True)
    class CartItemCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model=CartItem
            fields=('product','quantity')
    items=CartItemCreateSerializer(many=True)

    def create(self, validated_data):
        item_data=validated_data.pop('items')
        user=self.context['request'].user
        with transaction.atomic():
            cart=Cart.objects.create(user=user,**validated_data)
            for item in item_data:
                CartItem.objects.create(cart=cart,**item)

            return cart
        
    def update(self, instance, validated_data):
        item_data = validated_data.pop('items')
        instance = super().update(instance, validated_data)
        existing_items = {item.product_id: item for item in instance.items.all()}
        for item in item_data:
            product_id = item['product'].id 
            quantity = item['quantity']

            if product_id in existing_items:
                cart_item = existing_items[product_id]
                cart_item.quantity += quantity
                cart_item.save()
            else:

                CartItem.objects.create(cart=instance, product_id=product_id, quantity=quantity)
        return instance
                
    class Meta:
        model=Cart
        fields=('user','cart_id','checked_out','items')
        extra_kwargs = {
            'user': {'read_only': True}
        }
        

    