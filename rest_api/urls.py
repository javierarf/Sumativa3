from django.urls import path
from . import views 

urlpatterns = [
    path('usuarios/' , views.lista_usuarios , name='lista_usuarios'),
    path('consolas/', views.lista_consolas, name='lista_consolas'),
    path('consolas/<id>' , views.vista_consola , name='vista_consola')
]