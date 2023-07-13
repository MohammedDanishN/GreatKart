from django.urls import path

from .views import *

urlpatterns = [
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('password_reset/<uidb64>/<token>/',
         password_reset_validation, name='password_reset_validate'),
    path('forgotpassword/', forgotpassword, name='forgotpassword'),
    path('reset_password/', reset_password, name='reset_password'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
]
