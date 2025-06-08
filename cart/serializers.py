from rest_framework import serializers
from .models import Cart, CartItem
from django.db import transaction
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
        item_data = None
        if 'items' in validated_data:
            item_data = validated_data.pop('items')
        instance = super().update(instance, validated_data)
        existing_items = {item.product_id: item for item in instance.items.all()}
        print(existing_items)
        if item_data:
            for item in item_data:
                product_id = item['product'].id 
                quantity = item['quantity']
                print(product_id)

                if product_id in existing_items:
                    cart_item = existing_items[product_id]
                    if quantity> 0 and quantity <= cart_item.product.stock:
                        cart_item.quantity = quantity
                        cart_item.save()
                    elif quantity >= cart_item.product.stock:
                        raise serializers.ValidationError(
                        f"Requested quantity for '{cart_item.product.name}' exceeds available stock ({cart_item.product.stock})."
                    )
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