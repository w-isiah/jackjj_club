


from django.urls import path
from . import views

urlpatterns = [
    
    path("", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.account_profile, name="profile"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register_view/', views.register_view, name='register_view'),
    path("profile/", views.account_profile, name="profile"),
]
