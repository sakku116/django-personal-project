from django.shortcuts import render
from django.http import JsonResponse
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

    if request.method == "GET": # path:id (optional)
        if id:
            try:
                book_querySet = Book.objects.get(pk = id) # just one item
                result = book_querySet.as_dict() # as_dict() is user defined method in model class to serialize object
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
            # so, if want to retrieve data from json, it should be taken from request.body
            body_request = json.loads(request.body.decode('utf-8'))

            title = body_request['title']
            description = body_request['description']
        except:
            # data from html from or form encoded
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

    elif request.method == "DELETE": # path:id (required)
        try:
            book_querySet = Book.objects.get(id = id)
            item_obj = book_querySet.as_dict()

            # delete book
            book_querySet.delete()

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

    elif request.method == "PUT": # path:id & body request (required)
        try:
            body_request = json.loads(request.body.decode('utf-8'))

            title = body_request['title']
            description = body_request['description']
        except:
            title = None
            description = None

        try:
            book_querySet = Book.objects.get(id = id)
            
            if title:
                book_querySet.title = title
            if description:
                book_querySet.description = description

            book_querySet.save()

            status = 200
            message = 'book updated succesfully'
            success = True
        except:
            status = 400
            message = 'error'
            success = False
            
        return JsonResponse(
            {
                'success': success,
                'message': message,
            }, status = status
        )
            

