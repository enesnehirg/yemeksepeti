from rest_framework import serializers

from .models import Food


class FoodSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Food
        fields = [
            'id',
            'category',
            'name',
            'price'
        ]
