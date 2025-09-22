from django.urls import path
from . import views

urlpatterns = [
    path('contributions', views.contributions_list, name='contributions'),
    path("contributions/add/", views.add_contribution, name="add_contribution"),

    path('contributions/edit/<int:contribution_id>/', views.edit_contribution, name='edit_contribution'),
    path('contributions/delete/<int:contribution_id>/', views.delete_contribution, name='delete_contribution'),
    path('contributions/approve/<int:contribution_id>/', views.approve_contribution, name='approve_contribution'),
]


