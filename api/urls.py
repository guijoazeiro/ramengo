from django.urls import path
from .views import BrothList, ProteinList, OrderCreate

urlpatterns = [
    path('broths/', BrothList.as_view(), name='broth-list'),
    path('proteins/', ProteinList.as_view(), name='protein-list'),
    path('orders/', OrderCreate.as_view(), name='order-create'),
]
