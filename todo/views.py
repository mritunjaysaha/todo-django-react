from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from .models import Todo
from .serializers import TodoSerializer
from rest_framework.decorators import api_view


@api_view(['GET','POST','DELETE'])
def todo_list(request):
    if request.method == 'GET':
        todo = Todo.objects.all()
        title = request.GET.get('title', None)
        
        if title is not None:
            todo = todo.filter(title__icontains=title)
            
        todo_serializer = TodoSerializer(todo, many=True)
        return JsonResponse(todo_serializer.data, safe=False)
    elif request.method == 'POST':
        todo_data = JSONParser().parse(request)
        todo_serializer = TodoSerializer(data=todo_data)
        
        if todo_serializer.is_valid():
            todo_serializer.save()
            
            return JsonResponse(todo_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(todo_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET','PUT','DELETE'])
def todo_detail(request, pk):
    try:
        todo = Todo.objects.get(pk=pk)
    except Todo.DoesNotExist:
        return JsonResponse({'message': 'The tutorial does not exist'},status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        todo_serializer = TodoSerializer(todo)
        
        return JsonResponse(todo_serializer.data)
    elif request.method == 'PUT':
        todo_data = JSONParser().parse(request)
        todo_serializer = TodoSerializer(todo, data=todo_data)
        
        if todo_serializer.is_valid():
            todo_serializer.save()
            
            return JsonResponse(todo_serializer.data)
        return JsonResponse(todo_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        todo.delete()
        return JsonResponse({'message': 'Todo was deleted successfully'})
    