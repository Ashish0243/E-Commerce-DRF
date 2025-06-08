from rest_framework import serializers
from rating.models import Rating

class RatingSerializer(serializers.ModelSerializer):
    rating= serializers.IntegerField(min_value=1, max_value=5)
    class Meta:
        model= Rating
        fields = ('id', 'user', 'product', 'rating', 'review', 'created_at')
        extra_kwargs = {
            'id': {'read_only': True},
            'created_at': {'read_only': True}
        }