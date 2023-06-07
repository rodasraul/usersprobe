from django.shortcuts import render
# Importamos la funcion reverse para poder navegar o redirigir entre las funciones del sistema
from django.urls import reverse_lazy, reverse
# Importamos auth e importamos la funcion authenticate, login y logout
from django.contrib.auth import authenticate, login, logout
# Create your views here.
# Importamos funcion para redirigir
from django.http import HttpResponseRedirect
# la vista VIEW se utiliza para el LOGOUT por ser basico y elemental
from django.views.generic import (
    View, 
    CreateView,
)
from django.views.generic.edit import (
    FormView
)
# Importamos los formularios: UserRegisterForm y LoginForm
from .forms import UserRegisterForm, LoginForm
# Importamos el modelo
from .models import User

class UserRegisterView(FormView):
    template_name = 'users/register.html'
    # Trabajamos con un formulario FORMS.PY
    form_class = UserRegisterForm 
    success_url = '/'

    # 
    def form_valid(self, form):
        # Usamos el modelo USER y usamos el MANAGER con el metodo create_user
        # form.cleaned_data recuperamos datos del formulario
        User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            nombres=form.cleaned_data['nombres'],
            apellidos=form.cleaned_data['apellidos'],
            genero=form.cleaned_data['genero'],
        )
        # Sobreescribimos el metodo de la clase
        return super(UserRegisterView, self).form_valid(form)
    
# No usar para todo FORMVIEW, las otras vistas tambien sirven muchisimo
class LoginUser(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    # usamos reverse_lazy para dirigir la salida a otra vista por el nombre de la app
    success_url = reverse_lazy('home_app:panel')
    
    # Sobrescribe el metodo form_valid para validar los datos ingresados en el formulario
    def form_valid(self, form):
        """ El FORM_VALID sirve para validar el funcionamiento del LOGINUSER
        Recibe el username y password del formulario y lo guarda en la variable USER, 
        para ello utiliza la funcion authenticate
        Luego la funcion LOGIN utiliza los datos de la variable USER y los procesa
        en caso sean correctos los datos genera un login para todo el sistema
        """
        # Declaramos variable USER que contiene un usuario de la base de datos autenticado
        # se usa funcion authenticate, recibimos los campos del formulario
        # El campo a validar es el username, por ello se especifica dentro de authenticate
        # Si necesitamos validar con el Email debemos cambiar el campo username por email
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        # Funcion LOGIN 
        login(self.request, user)
        # El LOGIN se cumplirá recibiendo los datos del formulario en la variable USER y lo 
        # procesara la funcion login
        # Cuando se valide el usuario Django pasara a todo el sitio WEB un USUARIO que estará validado
        # Sobreescribimos la clase: super(nombre_de_clase, )
        return super(LoginUser, self).form_valid(form)

class LogoutView(View):
    """
    El Logout NO NECESITA template
    Puede sobreescribir otros metodos

    """
    def get(self, request, *args, **kwargs):
        logout(request)
        # Cuando complete el proceso de LOGOUT redirigira a la pantalla del LOGIN
        # Para redirigir se utiliza el HTTP, reverse es una funcion para navegar entre las opciones del sistema
        # DESPUES agregar en la plantilla del login, en el enlace de CERRAR, la URL para que se ejecute el LogoutView
        # user-logout {% url 'users_app:user-logout' %}
        return HttpResponseRedirect(
            reverse(
                'users_app:user-login'
            )
        )
