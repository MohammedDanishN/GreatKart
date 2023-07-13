from django.urls import path

from .views import *

urlpatterns = [
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout')
]
