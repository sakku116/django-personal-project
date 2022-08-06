from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt #, csrf_protect, requires_csrf_token
import json

from .models import Todo as todoModels

# Create your views here.
def crudTodo(request, id=None):
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