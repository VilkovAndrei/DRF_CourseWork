from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import UserCreateAPIView, UserRetrieveView, UserUpdateView, UserDeleteView, UserListView

app_name = UsersConfig.name

urlpatterns = [
    path('users/register/', UserCreateAPIView.as_view(), name='register'),
    path('users/detail/<int:pk>/', UserRetrieveView.as_view(), name='user-detail'),
    path('users/update/<int:pk>/', UserUpdateView.as_view(), name='user-update'),
    path('users/delete/<int:pk>/', UserDeleteView.as_view(), name='user-delete'),
    path('users_list/', UserListView.as_view(), name='users_list'),
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]