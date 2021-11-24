from rest_framework.generics import ListCreateAPIView, UpdateAPIView
from rest_framework import filters

from .models import Order
from .serializers import OrderSerializer


class OrderView(ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = []
    queryset = Order.objects.all()
    search_fields = ['status']
    filter_backends = (filters.SearchFilter,)


class CompleteOrderView(UpdateAPIView):
    serializer_class = OrderSerializer
    permission_classes = []
    queryset = Order.objects.all()

    def perform_update(self, serializer):
        serializer.save(status="Completed")
