from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import status
from tienda.models import Usuario, Consola
from .serializers import UsuarioSerializer, ConsolaSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate 

@csrf_exempt
@api_view(['POST'])
def login(request):
    data= JSONParser().parse(request)
    username = data['username']
    password = data['password']

    ##from django.contrib.auth.models import User
    ##user = User.objects.create_user(username='Pedro' , email='admin@gmail.com' , password='Pedro12345')
    ##user.save()
    
    if username is None or password is None:
        return Response('Se  requiere usuario y contraseña', status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username = username, password=password)
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response(token.key, status=status.HTTP_201_CREATED)
    else:
        return Response('Credenciales inválidas', status=status.HTTP_400_BAD_REQUEST)