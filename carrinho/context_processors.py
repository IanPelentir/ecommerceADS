from django.template.context_processors import request

from .car import Carrinho

def car(request):
    return {'car':Carrinho(request)}