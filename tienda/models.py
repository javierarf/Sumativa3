from django.db import models

# Create your models here.
class Usuario(models.Model):
    TIPO_USUARIO_CHOICES = [
        ('admin', 'Administrador'),
        ('visitante', 'Usuario Visitante'),
    ]

    nombres = models.CharField(max_length=200)
    apellidos = models.CharField(max_length=200)
    nombre_usuario = models.CharField(max_length=200, blank=True)
    correo_electronico = models.CharField(max_length=200, unique=True)
    contraseña = models.CharField(max_length=200)
    fecha_nacimiento = models.DateField()
    direccion = models.CharField(max_length=200, null=True, blank=True)
    tipo_usuario = models.CharField(max_length=10, choices=TIPO_USUARIO_CHOICES, default='visitante')

    def __str__(self):
        return self.nombre_usuario
    
class Marca_Consola(models.Model):
    Nombre_Marca = models.CharField(max_length=200)
    
    def __str__(self):
        return self.Nombre_Marca   
    
class Consola(models.Model):
    nombre_consola = models.CharField(max_length=200)
    modelo = models.CharField(max_length=200)
    especificaciones = models.TextField()
    caracteristicas = models.TextField()
    marca = models.ForeignKey(Marca_Consola, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='consolas/' , null=True)  # Campo para la imagen de la consola

    def __str__(self):
        return self.nombre_consola
    
    
    
