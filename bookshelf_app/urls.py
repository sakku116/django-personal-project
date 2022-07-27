from django.urls import path
from . import views

app_name = 'bookshelf_app'

urlpatterns = [
    path('api/books', views.getAllBooks, name='get-all-books'),
    path('api/book/<int:id>', views.getAllBooks, name='get-book'),
    path('api/create', views.createBook, name='create-book'),
]