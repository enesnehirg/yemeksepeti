import os
import json

from rest_framework.generics import ListCreateAPIView, UpdateAPIView
from rest_framework import filters
import redis

from .models import Order
from .serializers import OrderSerializer

r = redis.Redis(host=os.environ.get('REDIS_HOST'), port=6379)
p = r.pubsub()
p.subscribe('orders')


class OrderView(ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = []
    queryset = Order.objects.all()
    search_fields = ['status']
    filter_backends = (filters.SearchFilter,)

    def perform_create(self, serializer):
        serializer.save()
        order = json.dumps(serializer.data)
        r.publish('orders', order)


class CompleteOrderView(UpdateAPIView):
    serializer_class = OrderSerializer
    permission_classes = []
    queryset = Order.objects.all()

    def perform_update(self, serializer):
        serializer.save(status="Completed")
