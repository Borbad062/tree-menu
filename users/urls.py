from django.urls import path
from .views import UserCartView, UserLoginview, UserProfileView, UserRegistrationView, logout

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginview.as_view(), name='login'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('logout/', logout, name='logout'),
    path('users_cart/', UserCartView.as_view(), name='user_cart'),
]
