from django.shortcuts import render

# Create your views here.
from django.views.generic import(
    TemplateView
)


class HomePage(TemplateView):
    template_name = "home/index.html"
