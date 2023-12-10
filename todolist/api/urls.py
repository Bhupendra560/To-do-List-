from django.contrib import admin
from django.urls import path
from .views import TASKMODELVIEW

urlpatterns = [
    path('add/', TASKMODELVIEW.as_view(), name='add new task'),
    path('get/', TASKMODELVIEW.as_view(), name='get all tasks'),
    path('get/<int:pk>/', TASKMODELVIEW.as_view(), name='get any task'),
    path('update/<int:pk>/', TASKMODELVIEW.as_view(), name='update task'),
    path('delete/<int:pk>/', TASKMODELVIEW.as_view(), name='delete task')
]