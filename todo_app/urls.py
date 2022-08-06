from django.urls import path
from . import views

app_name = 'todo_app'

urlpatterns = [
    path('api/todo', views.crudTodo, name='crud-todo'),
    path('api/todo/<int:id>', views.crudTodo, name='crud-todo'),
]