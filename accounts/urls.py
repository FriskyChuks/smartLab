from django.contrib import admin
from django.urls import path
from .views import home, registration_view, login_view, logout_view, account_setting_view

urlpatterns = [
    path('', home, name='home'),
    path('accounts/registration/', registration_view, name='register'),
    path('accounts/login/', login_view, name='auth_login'),
    path("account_setting/<user_id>/", account_setting_view, name="account_setting"),
    path('accounts/logout/', logout_view, name='auth_logout'),

]
