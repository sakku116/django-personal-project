from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt #, csrf_protect, requires_csrf_token
import json

from .models import Book

# Create your views here.
def getAllBooks(request, id=None):
    if id:
        books_querySet = Book.objects.all().filter(id=id)
    else:
        books_querySet = Book.objects.all()

    result = []

    for book in books_querySet:
        result.append(book.as_dict()) # as_dict() is user defined method in model class to serialize object

    if len(result) == 1:
        # pop item from list if the list just contain 1 item
        result = result[0]

    return JsonResponse(
        {
            'books': result
        }
    )

@csrf_exempt
def createBook(request):
    if request.method == 'POST':
        # request.POST.get only retrieve data from form encoded
        try:
            body_request = json.loads(request.body.decode('utf-8'))
            title = body_request['title']
            description = body_request['description']
            print('data from json')
        except:
            title = request.POST.get('title')
            description = request.POST.get('description')
            print('data from form encoded')

        # try to create new object
        try:
            new_book = Book(title = title, description = description)
            new_book.save()
            message = 'success'
        except:
            message = 'failed'

    else:
        message = 'method is not supported. Use POST method instead!'

    return JsonResponse(
        {
            'message': message
        }
    )