from django.urls import path
from .views import RegisterUserView, LoginView, UserListView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='api-login'),
    path('users/', UserListView.as_view(), name='user-list'),
]
