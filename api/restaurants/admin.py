from django.contrib import admin

from .models import Restaurant, Category, Food

admin.site.register(Restaurant)
admin.site.register(Category)
admin.site.register(Food)
