from .models import Product,User, Category ,Cart, CartItem
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
            cart = Cart.objects.create(user=user, **validated_data)
            for item in item_data:
                product = item['product']
                quantity = item['quantity']
                if int(quantity) >= int(product.stock):
                    raise serializers.ValidationError(
                        f"Requested quantity for '{product.name}' exceeds available stock ({product.stock})."
                    )
                CartItem.objects.create(cart=cart, **item)
            return cart
        
    def update(self, instance, validated_data):
        item_data = validated_data.pop('items')
        print(f"item_data:{item_data}")
        instance = super().update(instance, validated_data)
        existing_items = {item.product_id: item for item in instance.items.all()}
        print(f"existing:data:{existing_items}")
        for item in item_data:
            product_id = item['product'].id 
            quantity = item['quantity']

            if product_id in existing_items:
                cart_item = existing_items[product_id]
                print(cart_item)
                if quantity> 0:
                    cart_item.quantity = quantity
                    print(cart_item)
                    cart_item.save()
                else:
                    cart_item.delete()
            else:
                if quantity > 0:
                    CartItem.objects.create(cart=instance, product_id=product_id, quantity=quantity)
        return instance
                
    class Meta:
        model=Cart
        fields=('user','cart_id','checked_out','items')
        extra_kwargs = {
            'user': {'read_only': True}
        }
        

    