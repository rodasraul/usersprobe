# Importamos el modelo
from django.db import models
# Importar BaseUserManager para poder sobreeescribir ciertas funciones necesarias
from django.contrib.auth.models import BaseUserManager

# Funciones especificas que traen AbstractBaseUser y PermissionsMixin y que se tienen que
# sobreescribir (BaseUsersManager, models.Manager) para conectar los managers
class UserManager(BaseUserManager, models.Manager):
    
    # Funcion privada:
    # self,
    # username, 
    # password, 
    # Un nuevo parametro llamado is_staff que determina si puede acceder al administrador de Django,
    # parametro is_superuser espcifica si el usuario que se esta creandose es un superusuario, 
    # **extra_fields diccionario para parametros adicionales
    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):

        # Creamos variable USER que esta haciendo el llamado al MODEL
        # Atributos que se necesitan para crear el usuario que es obligatorio
        # Para los atributos nombres y apellido se especifica en modelo como BLANK=TRUE para no obligatorios
        # is_staff y is_superuser ya los trae el AbstractBaseUser y lo estamos usando
        user = self.model(
            username=username,
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        # Para cifrar el password usamos el metodo set_password de la variable USER
        # set_password CIFRA HASHEA el password que se esta enviando
        user.set_password(password)
        # Grabamos el registro, self.db especificar en que base de datose se va a crear el usuario
        user.save(using=self.db)
        # Se ha creado correctamente el usuario
        return user
    
    # Sobreescribir funcion create_user, funcion es invocada cuando se cree un usuario normal
    # crea usuario con username, email, password, diccionario para atributos adicionales.
    def create_user(self, username, email, password=None, **extra_fields):
        # Para ahorrar codigo invocamos a la funcion privada
        # FALSE para is_straff y is_superuser
        return self._create_user(username, email, password, False, False, **extra_fields)
    
    # Sobreescribir funcion create_superuser, para crear superusuarios
    # parametros = (self, username, email, password=vacio, **extra_fields => cualquier otro atributo que se agregue para personalizar mas)
    def create_superuser(self, username, email, password=None, **extra_fields):
        # invocamos a funcion privada _create_user, con el username, para especificar que sea superusuario debemos especificar si es activo y si puede acceder al administrador
        # is_staff 
        # Pasamos True en lo parametros para is_staff y is_superuser para que los cree como superusuario
        return self._create_user(username, email, password, True, True, **extra_fields)

