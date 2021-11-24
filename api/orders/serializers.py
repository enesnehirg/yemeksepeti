from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Order, OrderItem
from api.restaurants.serializers import FoodSerializer, RestaurantSerializer


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
    orderitem_set = OrderItemSerializer(many=True, read_only=False, required=False)
    restaurant = RestaurantSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'restaurant',
            'status',
            'orderitem_set'
        ]

    def create(self, validated_data):
        orderitem_set = validated_data["orderitem_set"]
        order = Order.objects.create(
            user=validated_data["user"],
            restaurant=validated_data["restaurant"]
        )
        for orderitem in orderitem_set:
            print(orderitem)
            OrderItem.objects.create(
                food=orderitem["food"],
                quantity=orderitem["quantity"],
                order=order
            )
        return order
