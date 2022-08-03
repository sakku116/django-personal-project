from django.urls import path
from . import views

app_name = 'bookshelf_api_app'

urlpatterns = [
    path('', views.getAllBooks, name='get-all-books'),
    path('<int:id>', views.getAllBooks, name='get-book'),

    path('create/', views.createBook, name='create-book'),
]