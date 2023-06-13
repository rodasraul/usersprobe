import datetime

from django.shortcuts import render
# 1) Importar Mixin para validar si usuario esta logueado

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

# Create your views here.
from django.views.generic import(
    TemplateView
)

# MIXIN BASICO
# Para enviar una fecha
# object siempre se usa para los mixin
class FechaMixin(object):

    # get_context_data para enviar un contexto al template
    def get_context_data(self, **kwargs):
        context = super(FechaMixin, self).get_context_data(**kwargs)
        context['fecha'] = datetime.datetime.now()
        return context

# El LoginRequiredMixin necesita un atributo o propiedad
class HomePage(LoginRequiredMixin, TemplateView):
    template_name = "home/index.html"
    # Propiedad para saber que sucedera cuando detecte que el usuario NO esta logueado
    # Agregamos el reverse_lazy para que devuelva a la vista que corresponde en caso
    # NO este logueado
    login_url = reverse_lazy('users_app:user-login')


# TemplateView PruebaMixin
# Al declarar FechaMixin ya se puede reutilizar dentro de la Vista 
class TemplatePruebaMixin(FechaMixin, TemplateView):
    template_name = "home/mixin.html"

