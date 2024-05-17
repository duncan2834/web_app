from django.urls import path

from . import views

app_name = 'payment'

urlpatterns = [
    path('', views.CartView, name = 'cart'),
    path('orderplaced/', views.order_placed, name='order_placed'),
    path('webhook/', views.stripe_webhook),
]
