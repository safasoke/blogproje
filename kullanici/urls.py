from .views import register, user_login, user_logout, user_profile, user_settings, user_about, user_password_change
from django.urls import path, include, re_path

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='user-login'),
    path('logout/', user_logout, name='user-logout'),
    path('settings/', user_settings, name='user-settings'),
    path('password-change/', user_password_change, name='user-password-change'),
    re_path(r'(?P<username>[-\w]+)/about/$', user_about, name='user-aboutme'),
    re_path(r'(?P<username>[-\w]+)/$', user_profile, name='user-profile')

]
