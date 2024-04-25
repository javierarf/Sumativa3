from django import forms
from .models import Usuario , Consola

class formLog (forms.ModelForm):
    contraseña = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Usuario
        fields = ['nombre_usuario' , 'contraseña']

class EditarPerfilForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre_usuario']


class CambiarContrasenaForm(forms.Form):
    new_password = forms.CharField(label='Nueva Contraseña', widget=forms.PasswordInput)

class ConfirmarBorradoForm(forms.Form):
    confirmacion = forms.BooleanField(label='Confirmar el borrado', required=True)

class ConsolaForm(forms.ModelForm):
    class Meta:
        model = Consola
        fields = ['nombre_consola', 'modelo', 'especificaciones', 'caracteristicas', 'marca', 'imagen'] 

class VerificacionForm(forms.Form):
    nombre_usuario = forms.CharField(max_length=200)
    contraseña = forms.CharField(widget=forms.PasswordInput)

class ModificarPerfilForm(forms.ModelForm):
    contraseña = forms.CharField(widget=forms.PasswordInput)
    new_username = forms.CharField(max_length=200)  # Asegúrate de agregar este campo

    class Meta:
        model = Usuario
        fields = ['nombre_usuario', 'contraseña', 'new_username']

class RecuperarContraseñaForm(forms.Form):
    nombre_usuario = forms.CharField(label='Nombre de Usuario', max_length=200)
    correo_electronico = forms.EmailField(label='Correo Electrónico', max_length=200)

    def clean(self):
        cleaned_data = super().clean()
        nombre_usuario = cleaned_data.get('nombre_usuario')
        correo_electronico = cleaned_data.get('correo_electronico')
        
        try:
            usuario = Usuario.objects.get(nombre_usuario=nombre_usuario, correo_electronico=correo_electronico)
        except Usuario.DoesNotExist:
            raise forms.ValidationError('Usuario o correo electrónico incorrectos.')
        
        return cleaned_data        



