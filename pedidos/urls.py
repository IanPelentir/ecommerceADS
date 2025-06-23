from django.urls import path
from .views import PedidoCreateView, ResumoPedidoTemplateView, PedidosListView

urlpatterns = [
    path('criar/', PedidoCreateView.as_view(),
         name='novopedido'),
    path('meuspedidos/', PedidosListView.as_view(),
         name='meuspedidos'),
    path('resumo/<int:idpedido>/', ResumoPedidoTemplateView.as_view(),
         name='resumopedido'),

]