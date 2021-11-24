from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Category(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Food(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
