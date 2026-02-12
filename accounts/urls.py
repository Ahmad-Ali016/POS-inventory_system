from django.urls import path
from .views import RegisterUserView, UserListView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('users/', UserListView.as_view(), name='user-list'),
]