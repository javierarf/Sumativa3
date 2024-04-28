from django.shortcuts import render, redirect , get_object_or_404 
from tienda.models import Usuario , Consola , Marca_Consola
from .forms import formLog , EditarPerfilForm , ConfirmarBorradoForm , ConsolaForm , VerificacionForm ,ModificarPerfilForm , CambiarContrasenaForm , RecuperarContraseñaForm
from django.contrib import messages
import requests

# Create your views here.

def principal(request):
     return render(request, 'index.html' )

def home_admin(request):
    return render(request, 'AdminHome.html')

def Iniciar_Sesion(request):
    return render(request, 'Iniciar_Sesion.html')



def Nintendo(request):
    return render(request , 'Nintendo.html')

def NintendoSwichtOled(request):
    return render(request , 'NintendoSwicht-Oled.html')

def NintendoSwitchLite(request):
    return render(request , 'NintendoSwitchLite.html')

def NintendoSwitchNeon(request):
    return render(request , 'NintendoSwitchNeon.html')

def PlayStation(request):
    return render(request, 'PlayStation.html')

def PS5(request):
        return render(request , 'PS5.html')

def PS5Slim(request):
    return render(request , 'PS5-Slim.html')

def PS5SlimDig(request):
    return render(request , 'PS5-SlimDig.html')

def Registro(request):
    return render(request , 'Registro.html')

def Todos(request):
    return render(request , 'Todos.html')

def XboxSeriesSBlack(request):
    return render(request , 'Xbox-Series-S-Black.html')

def XboxSeriesSWhite(request):
    return render(request , 'Xbox-Series-S-White.html')

def XboxSeriesX(request):
    return render(request , 'Xbox-Series-X.html')


###REGISTRO DE USUARIO
def RegistrarUsuario(request):
    if request.method == 'POST':
        nom = request.POST['txtnom']
        ap = request.POST['txtap']
        nomus = request.POST['txtnomus']
        correo = request.POST['txtcorreo']
        contra = request.POST['txtcontra']
        naci = request.POST['txtnaci']
        direc = request.POST['txtdirec']
        
        # Obtener el tipo de usuario seleccionado
        tipo_usuario = request.POST.get('tipoUsuario', 'visitante')  
        
        Usser = Usuario(
            nombres=nom, 
            apellidos=ap, 
            nombre_usuario=nomus, 
            correo_electronico=correo, 
            contraseña=contra, 
            fecha_nacimiento=naci, 
            direccion=direc,
            tipo_usuario=tipo_usuario  
        )
        Usser.save()
        
        datos = {'correcto': 'Usuario Registrado Correctamente'}
        return render(request, 'Registro.html', datos)
    else:
        datos = {'fallo': 'Recuerde Rellenar Todos Los Campos'}
        return render(request, 'Registro.html', datos)
    

 ###Registro Usuario Pov Admin   
def RegistrarUsuarioAdmin(request):
    print("Entrando a la función RegistrarUsuarioAdmin")
    if request.method == 'POST':
        print("Método POST detectado")
        nom = request.POST['txtnom']
        ap = request.POST['txtap']
        nomus = request.POST['txtnomus']
        correo = request.POST['txtcorreo']
        contra = request.POST['txtcontra']
        naci = request.POST['txtnaci']
        direc = request.POST['txtdirec']
        
        # Obtener el tipo de usuario seleccionado
        tipo_usuario = request.POST.get('tipo_usuario', 'visitante')  
        print("Tipo de usuario seleccionado:", tipo_usuario)  # Debugging
        
        try:
            Usser = Usuario(
                nombres=nom, 
                apellidos=ap, 
                nombre_usuario=nomus, 
                correo_electronico=correo, 
                contraseña=contra, 
                fecha_nacimiento=naci, 
                direccion=direc,
                tipo_usuario=tipo_usuario  
            )
            Usser.save()
            datos = {'correcto': 'Usuario Registrado Correctamente'}
            return render(request, 'AdminHome.html', datos)
        except Exception as e:
            datos = {'fallo': 'Error al registrar el usuario'}
            return render(request, 'Registro_Admin.html', datos)
    else:
        datos = {'fallo': 'Recuerde Rellenar Todos Los Campos'}
        return render(request, 'Registro_Admin.html', datos)
    
###Login de usuarios     
def webLogin(request):
    mensaje_error = None
    nombre_usuario = None
    edit_form = EditarPerfilForm(request.POST)

    if request.method == 'POST':
        formulario = formLog(request.POST)
        if formulario.is_valid():
            usuario = formulario.cleaned_data['nombre_usuario']
            contraseña = formulario.cleaned_data['contraseña']

            verificacion = Usuario.objects.filter(nombre_usuario=usuario, contraseña=contraseña).exists()

            if verificacion:
                nombre_usuario = usuario
                perfil_usuario = Usuario.objects.get(nombre_usuario=usuario)
                
                if perfil_usuario.tipo_usuario == 'visitante':
                    return render(request, "Miperfil.html", {'nombre_usuario': nombre_usuario, 'perfil_usuario': perfil_usuario, 'edit_form': edit_form})
                elif perfil_usuario.tipo_usuario == 'admin':
                    # Renderizar la página para Administrador
                    return render(request, "AdminHome.html")
            else:
                mensaje_error = "Usuario o contraseña incorrectos. Inténtelo nuevamente."
    else:
        formulario = formLog()

    return render(request, 'Iniciar_Sesion.html', {'formLog': formulario, 'mensaje_error': mensaje_error, 'edit_form': edit_form})


###Modificacion de nombre de usuario###
def modificar_perfil(request):
    usuario = None
    form = VerificacionForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['nombre_usuario']
        password = form.cleaned_data['contraseña']
        
        try:
            usuario = Usuario.objects.get(nombre_usuario=username)
            if usuario.contraseña == password:
                # Contraseña correcta, mostrar el formulario de modificación
                form_modificacion = ModificarPerfilForm(instance=usuario)
                return render(request, 'modificarperfil.html', {'usuario': usuario, 'form_modificacion': form_modificacion})
            else:
                # Contraseña incorrecta, mostrar un mensaje de error
                mensaje_error = "La contraseña ingresada es incorrecta."
                return render(request, 'modificarperfil.html', {'form': form, 'mensaje_error': mensaje_error})
        
        except Usuario.DoesNotExist:
            mensaje_error = "El nombre de usuario ingresado no existe."
            return render(request, 'modificarperfil.html', {'form': form, 'mensaje_error': mensaje_error})

    return render(request, 'modificarperfil.html', {'form': form})

def guardar_cambios(request):
    if request.method == 'POST':
        form = ModificarPerfilForm(request.POST)
        
        if form.is_valid():
            nuevo_username = form.cleaned_data['new_username']  
            username = form.cleaned_data['nombre_usuario']
               
            try:
                usuario = Usuario.objects.get(nombre_usuario=username)
                usuario.nombre_usuario = nuevo_username
                usuario.save()

                messages.success(request, 'El nombre de usuario se ha actualizado correctamente.')
                return render(request, "Miperfil.html", {'perfil_usuario': usuario})
            
            except Usuario.DoesNotExist:
                messages.error(request, 'El nombre de usuario ingresado no existe.')
                pass
        else:
            # En caso de que el formulario no sea válido, manejar los errores o mostrarlos
            messages.error(request, 'El formulario no es válido.')
            return render(request, 'modificarperfil.html', {'form': form})

    return redirect('modificar_perfil')


###Modificacion de contraseña###
def modificar_contrasena(request):
    usuario = None
    form = VerificacionForm()
    
    if request.method == 'POST':
        form = VerificacionForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['nombre_usuario']
            contraseña = form.cleaned_data['contraseña']
            
            try:
                usuario = Usuario.objects.get(nombre_usuario=username)
                
                if usuario.contraseña == contraseña:
                    form_cambio = CambiarContrasenaForm(initial={'username': username})
                    return render(request, 'Modificarcontra.html', {'usuario': usuario, 'form_cambio': form_cambio})
                else:
                    messages.error(request, 'La contraseña ingresada es incorrecta.')
                    
            except Usuario.DoesNotExist:
                messages.error(request, 'El nombre de usuario ingresado no existe.')
                
    return render(request, 'Modificarcontra.html', {'form': form})

def guardar_cambios_contrasena(request):
    if request.method == 'POST':
        form = CambiarContrasenaForm(request.POST)
        username = request.POST.get('username')
        
        if form.is_valid():
            nueva_contraseña = form.cleaned_data['new_password']
            
            try:
                usuario = Usuario.objects.get(nombre_usuario=username)
                usuario.contraseña = nueva_contraseña
                usuario.save()

                messages.success(request, 'Contraseña actualizada correctamente.')
                return render(request, "Miperfil.html", {'perfil_usuario': usuario})
                
            except Usuario.DoesNotExist:
                messages.error(request, 'El nombre de usuario ingresado no existe.')
                
    return redirect('modificar_contrasena')


###Eliminar usuario en la base de datos###
def borrar_perfil(request):
    usuario = None
    form = VerificacionForm()
    
    if request.method == 'POST':
        form = VerificacionForm(request.POST)
        if form.is_valid():
            nombre_usuario = form.cleaned_data['nombre_usuario']
            contraseña = form.cleaned_data['contraseña']
            try:
                usuario = Usuario.objects.get(nombre_usuario=nombre_usuario)
                if usuario.contraseña == contraseña:
                    return render(request, 'Eliminarusuario.html', {'form_confirmacion': ConfirmarBorradoForm(), 'usuario': usuario})
                else:
                    mensaje_error = "Contraseña incorrecta."
                    return render(request, 'Eliminarusuario.html', {'form': form, 'mensaje_error': mensaje_error})
            except Usuario.DoesNotExist:
                mensaje_error = "Usuario no encontrado."
                return render(request, 'Eliminarusuario.html', {'form': form, 'mensaje_error': mensaje_error})
    
    return render(request, 'Eliminarusuario.html', {'form': form})

def confirmar_borrar_perfil(request):
    if request.method == 'POST':
        form = ConfirmarBorradoForm(request.POST)
        
        if form.is_valid():
            confirmacion = form.cleaned_data['confirmacion']
            
            if confirmacion:
                username = request.POST.get('username')
                try:
                    usuario = Usuario.objects.get(nombre_usuario=username)
                    usuario.delete()  # Elimina el usuario de la base de datos
                    return render(request, 'perfil_eliminado.html')  # Renderiza una página de confirmación de eliminación
                except Usuario.DoesNotExist:
                    mensaje_error = "Usuario no encontrado."
                    return render(request, 'Eliminarusuario.html', {'mensaje_error': mensaje_error})
            else:
                mensaje_error = "Debe confirmar la eliminación."
                form.add_error('confirmacion', mensaje_error)  # Agrega el mensaje de error al formulario
                return render(request, 'Eliminarusuario.html', {'form_confirmacion': form})
        else:
            print("Errores en el formulario:", form.errors)  # Debugging
    
    return redirect('borrar_perfil')


###RECUPERAR CONTRASEÑA
def recuperar_contraseña(request):
    form = RecuperarContraseñaForm()
    contraseña = None
    
    if request.method == 'POST':
        form = RecuperarContraseñaForm(request.POST)
        if form.is_valid():
            nombre_usuario = form.cleaned_data['nombre_usuario']
            usuario = Usuario.objects.get(nombre_usuario=nombre_usuario)
            contraseña = usuario.contraseña  

    return render(request, 'RecuperarContraseña.html', {'form': form, 'contraseña': contraseña})

###APARTADO ADMIN CRUD CONSOLAS
###Agregar consola
def agregar_consola(request):
    if request.method == 'POST':
        form = ConsolaForm(request.POST, request.FILES)  
        if form.is_valid():
            form.save()
            return render(request,'AdminHome.html')  
    else:
        form = ConsolaForm()

    return render(request, 'AdminAgregarConsola.html', {'form': form})

###Ver Consola
def ver_consolas(request):
    consolas = Consola.objects.all()  
    return render(request, 'AdminVerConsolas.html', {'consolas': consolas})

##Borrar consola
def borrar_consola(request, consola_id):
    consola = Consola.objects.get(id=consola_id)
    consola.delete()
    return redirect('ver_consolas')

##Editar consola
def editar_consola(request, consola_id):
    consola = get_object_or_404(Consola, id=consola_id)

    if request.method == 'POST':
        form = ConsolaForm(request.POST, request.FILES, instance=consola)
        if form.is_valid():
            form.save()
            return redirect('ver_consolas')
    else:
        form = ConsolaForm(instance=consola)

    return render(request, 'AdminEditarConsola.html', {'form': form})



###Vista Usuarios consola Playstation
def PlayStation(request):
    # Obtener la marca PlayStation
    marca_playstation = Marca_Consola.objects.get(Nombre_Marca='PlayStation')
    
    # Obtener las consolas de la marca PlayStation
    consolas_playstation = Consola.objects.filter(marca=marca_playstation)
    
    context = {
        'consolas_playstation': consolas_playstation,
    }
    
    return render(request, 'PlayStation.html', context)

###Vista usuario consola Microsoft
def Microsoft(request):
    # Obtener la marca Microsoft
    marca_microsoft = Marca_Consola.objects.get(Nombre_Marca='Microsoft')
    
    # Obtener las consolas de la marca Microsoft
    consolas_microsoft = Consola.objects.filter(marca=marca_microsoft)
    
    context = {
        'consolas_microsoft': consolas_microsoft,
    }
    
    return render(request, 'Microsoft.html', context)

###Vista usuario consola Nintendo
def Nintendo(request):
    # Obtener la marca Nintendo
    marca_nintendo = Marca_Consola.objects.get(Nombre_Marca='Nintendo')
    
    # Obtener las consolas de la marca Nintendo
    consolas_nintendo = Consola.objects.filter(marca=marca_nintendo)
    
    context = {
        'consolas_nintendo': consolas_nintendo,
    }
    
    return render(request, 'Nintendo.html', context)

###Todas las Consolas
def Todos(request):
    # Obtener todas las consolas
    consolas = Consola.objects.all()
    
    context = {
        'consolas': consolas,
    }
    
    return render(request, 'Todos.html', context)

###Detale generico de las consolas
def detalle_consola(request, consola_id):
    consola = get_object_or_404(Consola, id=consola_id)
    return render(request, 'detalle_consola.html', {'consola': consola})


def lista_juegos(request):
    url = 'https://www.freetogame.com/api/games'
    response = requests.get(url)

    juegos = response.json()

    context = {
        'juegos' : juegos
    }

    return render(request,'juegos.html', context)

def API_Figuras(request):
    return render(request, 'API_Figuras.html' )
