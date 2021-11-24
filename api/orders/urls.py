from django.urls import path

from .views import OrderView, CompleteOrderView

urlpatterns = [
    path('orders/', OrderView.as_view()),
    path('complete-order/<slug:pk>/', CompleteOrderView.as_view()),
]
