from rest_framework import serializers

from product.models import Category, Product


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
        fields=('id','name','description','price','stock','category','image')
        extra_kwargs = {
            'id': {'read_only': True}
        }
    
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value
    
class ProductListSerializer(serializers.ModelSerializer):
    category= CategorySerializer(read_only=True)
    class Meta:
        model= Product
        fields=('id','name','description','price','stock','category','avg_rating', 'image')
        extra_kwargs = {
            'id': {'read_only': True}
        }
    
    