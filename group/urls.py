from django.urls import path
from . import views

urlpatterns = [
    path('', views.group_list, name='group_list'),
    path('create/', views.group_create, name='group_create'),
    path('<int:pk>', views.group_detail, name='group_detail'),
    path('update/<int:pk>', views.group_update, name='group_update'),
    path('delete/<int:pk>', views.group_delete, name='group_delete'),
]
