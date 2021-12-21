from django.urls import path

from .views import login_user, register_end_user

urlpatterns = [
    # All User routes. All routes concern User data and User Model
    path('register/', register_end_user, name='api.register_end_user'),
    path('login/', login_user, name='api.login_user'),
]
