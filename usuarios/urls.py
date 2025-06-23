from django.urls import path
from .views import UsuarioCreateView


urlpatterns = [
    path('novo/', UsuarioCreateView.as_view(),
         name='cadusuario'),
]