from users.apps import UsersConfig
from django.urls import path

from users.views import UserCreateView, email_verification, LoginView, LogoutView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserCreateView.as_view(), name='register'),
    path('email_confirm/<str:token>', email_verification, name='email_confirm'),
]