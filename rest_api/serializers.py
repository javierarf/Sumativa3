from rest_framework import serializers
from tienda.models import Usuario , Marca_Consola , Consola

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model=Usuario
        fields=['nombres' , 'apellidos' , 'nombre_usuario' , 'correo_electronico' , 'contraseña' , 'fecha_nacimiento' , 'direccion' , 'tipo_usuario']


class Marca_ConsolaSerializer(serializers.ModelSerializer):
    class Meta :
        model= Marca_Consola
        fields=['Nombre_Marca']

class ConsolaSerializer(serializers.ModelSerializer):
    class Meta :
        model= Consola
        fields=['id','nombre_consola' , 'modelo' , 'especificaciones' , 'caracteristicas' , 'marca' , 'imagen']

