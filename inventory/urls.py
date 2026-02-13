from django.urls import path

from .views import (
    ProductCreateView, ProductListView, ProductDetailView, CategoryListCreateView, CategoryDetailView,
    StockAlertView,
    )

urlpatterns = [
    # GET (list) or POST (create)
    path('add/', ProductCreateView.as_view(), name='product-add'),
    path('list/', ProductListView.as_view(), name='product-list'),
    # GET, PUT, PATCH, DELETE - Specific item by ID
    path('detail/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),

    # Categories urls
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),

    path('stock-report/', StockAlertView.as_view(), name='stock-report'),
]
