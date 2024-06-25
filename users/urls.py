from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import UserCreateAPIView, UserRetrieveView, UserUpdateView, UserDeleteView, UserListView, \
    MyTokenObtainPairView

app_name = UsersConfig.name

urlpatterns = [
    path('users/register/', UserCreateAPIView.as_view(), name='register'),
    path('users/detail/<int:pk>/', UserRetrieveView.as_view(), name='user_detail'),
    path('users/update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('users/delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
    path('users/list/', UserListView.as_view(), name='users_list'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]