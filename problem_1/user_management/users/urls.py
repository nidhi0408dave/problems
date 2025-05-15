from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_users, name='list_users'),
    path('add/', views.add_user, name='add_user'),
    path('delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('export/', views.export_users_pdf, name='export_users_pdf'),
]
