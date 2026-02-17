from django.urls import path
from purchases.views import VendorListCreateView, AllVendorsListView, ProcessSupplyView, VendorPurchaseHistoryView

urlpatterns = [
    path('vendors/', VendorListCreateView.as_view(), name='vendor-list-create'),
    path('vendors/list/', AllVendorsListView.as_view(), name='all-vendors-list'),
    path('process-supply/', ProcessSupplyView.as_view(), name='process-supply'),
    path('history/', VendorPurchaseHistoryView.as_view(), name='purchase-history'),
]