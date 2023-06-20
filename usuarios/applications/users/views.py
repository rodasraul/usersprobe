from django.shortcuts import render
# funcio para enviar correo
from django.core.mail import send_mail
# 1) Importamos Mixin para validar si usuario esta logueado
from django.contrib.auth.mixins import LoginRequiredMixin
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
from .forms import (
    UserRegisterForm,
    LoginForm,
    UpdatePasswordForm,
    VerificationForm
)
# Importamos el modelo
from .models import User

from .functions import code_generator

#class UserRegisterView(LoginRequiredMixin, FormView):
class UserRegisterView(FormView):
    template_name = 'users/register.html'
    # 2) Agregamos MIXIN para que valide si tenemos usuario logueado.
    # login_url = reverse_lazy('users_app:user-login')

    # Trabajamos con un formulario FORMS.PY
    form_class = UserRegisterForm 
    success_url = '/'

    # 
    def form_valid(self, form):
        # Importamos el codigo que se enviará por correo
        codigo = code_generator()

        # Usamos el modelo USER y usamos el MANAGER con el metodo create_user
        # form.cleaned_data recuperamos datos del formulario
        User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            nombres=form.cleaned_data['nombres'],
            apellidos=form.cleaned_data['apellidos'],
            genero=form.cleaned_data['genero'],
            codregistro=codigo
        )
        # Enviar el codigo al email del usuario
        asunto = 'Confirmacion de email'
        mensaje = '<h1>Codigo de verificacion: ' + codigo + '</h1>'
        email_remitente = 'raul@rhodasingenieria.com'
        # enviando el correo
        send_mail(asunto, mensaje, email_remitente, [form.cleaned_data['email'],])
        # Redirigir a pantalla de validacion

        # Sobreescribimos el metodo de la clase
        # Esta linea nos envia al sucess_url que esta al inicio de la clase
        # La estamos comentando porque ahora se dirigira a otra pantalla de validacion del codigo para el correo electronico
        # return super(UserRegisterView, self).form_valid(form)

        return HttpResponseRedirect(
            reverse(
                'users_app:user-verification'
            )
        )
    
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

class UpdatePasswordView(LoginRequiredMixin, FormView):
    template_name = 'users/update.html'
    login_url = reverse_lazy('users_app:user-login')
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('users_app:user-login')

    def form_valid(self, form):
        # Recuperar usuario validado del sistema
        usuario = self.request.user
        # Obtener los datos para hacer la autenticacion
        # De la ariable usuario obtengo el username
        # Recuperamos desde el formulario el password ingresado
        user = authenticate(
            username=usuario.username,
            password=form.cleaned_data['password1']
        )
        # Si la autenticacion es correcta en la variable user ya existen datos
        if user:
            new_password = form.cleaned_data['password2']
            # Encripta la contraseña 
            usuario.set_password(new_password)
            # Guardamos los datos
            usuario.save()
        
        # Con logout se cierra el sistema y se vuelve al login, por seguridad
        logout(self.request)
        return super(UpdatePasswordView, self).form_valid(form)

class CodeVerificationView(FormView):
    template_name = 'users/verification.html'
    form_class = VerificationForm
    success_url = reverse_lazy('users_app:user-login')
    
    def form_valid(self, form):
        return super(CodeVerificationView, self).form_valid(form)

