from django.urls import path
from . import api_views

app_name = 'bookshelf_app'

urlpatterns = [
    path('api/book', api_views.crudBook, name='crud-book'),
    path('api/book/<int:id>', api_views.crudBook, name='crud-book'),
]