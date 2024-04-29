from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import status
from tienda.models import Usuario, Consola
from .serializers import UsuarioSerializer, ConsolaSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# Create your views here.
@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def lista_usuarios(request):
    if request.method== 'GET':
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios , many=True)

    return Response(serializer.data)


@csrf_exempt
@api_view(['GET' , 'POST'])
@permission_classes((IsAuthenticated,))
def lista_consolas(request):
    if request.method== 'GET':
        consolas = Consola.objects.all()
        serializer = ConsolaSerializer(consolas , many=True)

        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ConsolaSerializer(data = data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

@csrf_exempt
@api_view(['GET' , 'PUT' , 'PATCH' , 'DELETE']) 
@permission_classes((IsAuthenticated,))     
def vista_consola(request , id):  

    try:
        consola = Consola.objects.get(id=id)
    except Consola.DoesNotExist: 
       return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ConsolaSerializer(consola)
        return Response(serializer.data)
    
    elif request.method == 'PUT' or request.method == 'PATCH':
        serializer = ConsolaSerializer(consola, data=request.data)
     
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        consola.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)    





