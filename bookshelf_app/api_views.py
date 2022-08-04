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
    message = None
    success = False
    status = 200

    if request.method == 'POST':
        # request.POST.get only retrieve data from form encoded
        try:
            body_request = json.loads(request.body.decode('utf-8'))
            title = body_request['title']
            description = body_request['description']
            print(f'data from json = {title, description}')
        except:
            title = request.POST.get('title')
            description = request.POST.get('description')
            print(f'data from form encoded = {title, description}')

        # try to create new object
        try:
            new_book = Book(title = title, description = description)
            new_book.save()

            success = True
            status = 200
            message = f"success creating a '{title}' book (description = '{description}')"
        except:
            success = False
            status = 400
            message = "'title' and 'description' are required!"

    else:
        success = False
        status = 400
        message = 'method is not supported. Use POST method instead!'

    return JsonResponse(
        {
            'success': success,
            'message': message,
        }, status = status
    )

@csrf_exempt
def deleteBook(request, id):
    success = False
    message = None
    status = 200

    if request.method == "DELETE":
        try:
            query = Book.objects.get(id = id)
            item_obj = query.as_dict()

            # delete book
            query.delete()

            status = 200
            message = f'book deleted successfully'
            success = True        
        except:
            status = 400
            message = "failed to delete the book"
            success = False
    else:
        status = 400
        message = "request method is not supported. use DELETE method instead!"
        succces = False

    return JsonResponse(
        {
            'success' : success,
            'message' : message
        }, status = status
    )