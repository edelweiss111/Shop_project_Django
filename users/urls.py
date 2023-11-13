from django.urls import path
from users.apps import UsersConfig
from users.views import LoginUserView, LogoutUserView, RegisterUserView, verification, Verify

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('verify/', Verify.as_view(), name='verify'),
    path('verification/<str:code>/', verification, name='verification'),

    ]
