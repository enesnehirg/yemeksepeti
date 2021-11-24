from django.db import models
from django.contrib.auth.models import User

from .constants import STATUS_CHOICES
from api.restaurants.models import Restaurant, Food


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICES, max_length=9, default=STATUS_CHOICES[0][0])

    def __str__(self):
        return 'User: ' + self.user.username+ ' | Restaurant: ' + self.restaurant.name


class OrderItem(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
