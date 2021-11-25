from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Order, OrderItem
from api.restaurants.models import Restaurant
from api.restaurants.serializers import FoodSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "food",
            "quantity",
            "order",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        food_serializer = FoodSerializer(instance.food)
        data['food'] = food_serializer.data
        return data


class OrderSerializer(serializers.ModelSerializer):
    orderitem_set = OrderItemSerializer(many=True, required=True)
    restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects)

    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'restaurant',
            'status',
            'orderitem_set'
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        restaurant = instance.restaurant.name
        user_serializer = UserSerializer(instance.user)
        data['restaurant'] = restaurant
        data['user'] = user_serializer.data
        return data

    def create(self, validated_data):
        order = Order.objects.create(
            user=validated_data["user"],
            restaurant=validated_data["restaurant"]
        )
        if "orderitem_set" in validated_data:
            orderitem_set = validated_data["orderitem_set"]
            for orderitem in orderitem_set:
                OrderItem.objects.create(
                    food=orderitem["food"],
                    quantity=orderitem["quantity"],
                    order=order
                )
        return order
