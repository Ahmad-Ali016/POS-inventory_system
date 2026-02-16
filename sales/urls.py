from django.urls import path
from .views import RegisterView, LoginView, CustomerListView, ProcessSaleView, SaleListView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('customers/', CustomerListView.as_view(), name='customer-list'),
    path('process-sale/', ProcessSaleView.as_view(), name='process-sale'),
    path('transactions/', SaleListView.as_view(), name='sale-list'),
]