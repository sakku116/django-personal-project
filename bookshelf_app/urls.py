from django.urls import path
from . import api_views

app_name = 'bookshelf_app'

urlpatterns = [
    path('api/books', api_views.getAllBooks, name='get-all-books'),
    path('api/book/<int:id>', api_views.getAllBooks, name='get-book'),
    path('api/create', api_views.createBook, name='create-book'),
    path('api/delete/<int:id>', api_views.deleteBook, name='delete-book')
]