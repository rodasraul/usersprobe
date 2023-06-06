from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
# Importamos el MANAGERS.PY para conectarlo con el MODELO
from .managers import UserManager

# Create your models here.
# PermissionsMixin => Para hacernos cargo de la creacion de superusuarios desde consola
# Esto nos ayuda en personalizar por completo el modelo de usuarios de Django
class User(AbstractBaseUser, PermissionsMixin):
    """Definicion del Modelo para USER."""
    GENDER_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otros'),
    )

    username = models.CharField(max_length=10, unique=True)
    email = models.EmailField()
    nombres = models.CharField(max_length=30, blank=True)
    apellidos = models.CharField(max_length=30, blank=True)
    genero = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    # AbstractBaseUser obliga a crear el atributo is_staff en el modelo actual, por default es FALSE
    is_staff = models.BooleanField(default=False)
    # Especificar cual atributo para hacer el login desde el Administrador
    USERNAME_FIELD = 'username'
    # Especificar Campos que SOLICITAR  ingresar al crear un usuario
    REQUIRED_FIELDS = ['email', 'nombres', 'apellidos', 'genero', ]
    # conectamos el MANAGER con el MODELO
    objects = UserManager()

    # TODO: Define fields here

    class Meta:
        """Meta definition for MODELNAME."""

        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def get_short_name(self):
        return self.username
    
    def get_full_name(self):
        return self.nombres + ' ' + self.apellidos
