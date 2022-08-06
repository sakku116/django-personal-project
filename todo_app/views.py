from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt #, csrf_protect, requires_csrf_token
import json

from .models import Todo as todoModels

# Create your views here.
def crudTodo(request, id=None):
    # default response
    status = 200
    message = None
    success = True

    if request.method == "GET":
        if id:
            try:
                todo_querySet = todoModels.objects.get(pk = id)
                result = todo_querySet.as_dict()
            except:
                result = None
        else:
            todos_querySet = todoModels.objects.all()
            result = []
            for todo in todos_querySet:
                result.append(todo.as_dict())

            if len(result) == 0:
                result = None

        return JsonResponse(result, safe=False)

    elif request.method == "POST":
        try:
            # data from json data
            json_data = json.loads(request.body.decode('utf-8'))
            name = json_data['name']
        except:
            # data from 'form encoded'
            name = request.POST.get('name')
        
        try:
            new_todo = todoModels.objects.create(name = name)
            new_todo.save()

            message = 'new todo created succesfully'
        except:
            status = 400
            message = "'name' required"
            success = False

        return JsonResponse(
            {
                'success': success,
                'message': message
            }, status = status
        )

    elif request.method == "DELETE":
        if id:
            todo_item = None

            try:
                todo_querySet = todoModels.objects.get(pk = id)
                todo_item = todo_querySet.as_dict()

                todo_querySet.delete()

                message = 'successfully delete todo item'
            except:
                success = False
                message = 'failed to delete todo item'
                status = 400

            return JsonResponse(
                {
                    'success': success,
                    'message': message,
                    'deleted_todo_item': todo_item,
                }, status = status
            )

        else:
            return JsonResponse(
                {
                    'success': False,
                    'message': '"id" path parameter is required!',
                }, status = 400
            )

    elif request.method == "PUT":
        if id:
            data_before_update = None
            data_after_update = None

            # get body request
            try:
                # data from json data
                json_data = json.loads(request.body.decode('utf-8'))
                name = json_data['name']
            except:
                # data from 'form encoded'
                name = request.POST.get('name')

            # execute query
            try:
                todo_querySet = todoModels.objects.get(pk = id)

                data_before_update = todo_querySet.as_dict()

                todo_querySet.name = name
                todo_querySet.save()

                data_after_update = todo_querySet.as_dict()

                message = 'todo item updated successfully'
            except:
                status = 400
                message = 'error'
                success = False

            return JsonResponse(
                {
                    'success': success,
                    'message': message,
                    'data_before_update': data_before_update,
                    'data_after_update': data_after_update,
                }, status  = status
            )

        else:
            return JsonResponse(
                {
                    'success': False,
                    'message': '"id" path parameter is required!',
                }, status = 400
            )