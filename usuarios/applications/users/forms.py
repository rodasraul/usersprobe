from django import forms

from .models import User

class UserRegisterForm(forms.ModelForm):
    # Para que se ingrese la contraseña en el formulario, retornará cifrada NO PLANA
    password1 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña'
            }
        )
    )
    password2 = forms.CharField(
        label='Contraseña (Repetir)',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Repetir contraseña'
            }
        )
    )

    class Meta:
        # vinculamos al modelo
        model = User
        # Para traer todos los campos
        # fields = ('__all__')
        # Especificamos los campos que veremos en el formulario
        fields = (
            'username',
            'email',
            'nombres',
            'apellidos',
            'genero',
        )

    # Validar si los password son DIFERENTES
    # self.add_error especifica en que CAMPO aparece el mensaje de error
    def clean_password2(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            self.add_error('password2', 'Las contraseñas no son iguales')

# Formulario de LOGIN
# Se hereda de forms.ModelForm porque se extrae directamente del MODELO
# Se usa forms.Form para crear el formulario a libertad, sin depender de un MODELO
class LoginForm(forms.Form):
    # Campo USERNAME, 
    username = forms.CharField(
        label='Usuario',
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Usuario',
                'style': '{ margin: 10px }',
            }
        )
    )
    # Campo password
    password = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña',
                'style': '{ margin: 10px }',
            }
        )
    )

    # SE PUEDE HACER QUE AQUI SE VERIFIQUE SI EL USUARIO ES O NO ES USUARIO VALIDO