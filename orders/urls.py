
from django.urls import path
from . import views


urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('payments/', views.payments, name='payments'),
    path('create-order/', views.create_order, name='create-order'),
    path('verify-payment/', views.verify_payment, name='verify-payment'),
    path('payment_success/', views.payment_success, name='payment_success'),
]
