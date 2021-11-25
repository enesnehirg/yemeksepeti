from django.test import TestCase
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.test import APIClient

from api.restaurants.models import Restaurant, Food, Category
from .models import Order, OrderItem

client = APIClient()
client.default_format = 'json'


class OrderTestCase(TestCase):
    """
    - setUp function runs before every test method to set up all needed objects.
    - Changing methods order or implementing new test methods between them will cause errors because primary key related
    fields' ids will be changed.
    """
    def setUp(self):
        password = get_random_string(8)
        user = User.objects.create_user(username="uozy", email="uozy@yspt.com", password=password)
        restaurant = Restaurant.objects.create(name="Super Donerci")
        category = Category.objects.create(title="Doner/Kebap")
        Food.objects.create(name="Doner", category=category, restaurant=restaurant, price=45.5)
        Food.objects.create(name="Iskender", category=category, restaurant=restaurant, price=55.5)
        Order.objects.create(user=user, restaurant=restaurant)

    def test_create_order(self):
        data = {
            "user": 2,
            "restaurant": 2,
            "orderitem_set": [
                {
                    "food": 3,
                    "quantity": 3
                },
                {
                    "food": 4,
                    "quantity": 1
                }
            ]
        }
        response = client.post('/api/v1/orders/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        order_id = response.data['id']
        order = Order.objects.get(id=order_id)
        self.assertEqual(Order.objects.count(), 2)
        self.assertEqual(order.restaurant.id, 2)
        self.assertEqual(OrderItem.objects.count(), 2)
        self.assertEqual(OrderItem.objects.get(id=1).order, order)

    def test_list_orders(self):
        # List pending orders
        response = client.get('/api/v1/orders/?search=Pending')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['status'], "Pending")
        # List completed orders
        response = client.get('/api/v1/orders/?search=Completed')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
        data = {
            "user": 3,
            "restaurant": 3,
            "orderitem_set": [
                {
                    "food": 5,
                    "quantity": 6
                }
            ]
        }
        response = client.post('/api/v1/orders/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        order_id = response.data['id']
        order = Order.objects.get(id=order_id)
        order.status = "Completed"
        order.save()
        response = client.get('/api/v1/orders/?search=Completed')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['status'], "Completed")
        # List all orders
        response = client.get('/api/v1/orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_complete_order(self):
        order = Order.objects.filter().first()
        response = client.patch('/api/v1/complete-order/%s/' % order.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], "Completed")
