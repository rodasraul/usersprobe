# Funciones extra de la aplicacion USERS

import random
import string

def code_generator(size=6, chars=string.ascii_uppercase + string.digits):
    # Genera un codigo de 6 numeros
    return ''.join(random.choice(chars) for _ in range(size))
