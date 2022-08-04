from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt #, csrf_protect, requires_csrf_token
import json

from .models import Book

# Create your views here.
@csrf_exempt
def crudBook(request, id=None):
    # default response
    status = 200
    message = None
    success = True

    if request.method == "GET": # id (optional)
        if id:
            try:
                books_querySet = Book.objects.get(pk = id) # just one item
                result = books_querySet.as_dict() # as_dict() is user defined method in model class to serialize object
            except:
                result = None
        else:
            books_querySet = Book.objects.all() # more than one
            result = []

            for book in books_querySet:
                result.append(book.as_dict())

            if len(result) == 1:
                # pop item from list if the list just contain 1 item
                result = result[0]

        return JsonResponse(result, safe = False)

    elif request.method == 'POST': # body request (required)
        try:
            # request.POST.get only retrieve data from form encoded
            body_request = json.loads(request.body.decode('utf-8'))

            title = body_request['title']
            description = body_request['description']
        except:
            title = request.POST.get('title')
            description = request.POST.get('description')

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

        return JsonResponse(
            {
                'success': success,
                'message': message,
            }, status = status
        )

    elif request.method == "DELETE": # id (required)
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

        return JsonResponse(
            {
                'success' : success,
                'message' : message
            }, status = status
        )
