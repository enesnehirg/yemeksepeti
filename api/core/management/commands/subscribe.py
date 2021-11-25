import json

from rest_framework.test import APIClient
from django.core.management.base import BaseCommand
import redis


class Command(BaseCommand):
    def handle(self, *args, **options):
        client = APIClient()
        r = redis.Redis(host='redis', port=6379)
        p = r.pubsub()
        p.subscribe('orders')

        for message in p.listen():
            if message:
                if message.get("type") == "message":
                    print("New order has arrived!")
                    data = json.loads(message.get('data', ''))
                    client.patch('/api/v1/complete-order/%s/' % data["id"])
                    print("Order is completed!")
