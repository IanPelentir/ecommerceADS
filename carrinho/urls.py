from django.urls import path
from . import views

urlpatterns = [
    path('', views.CarrinhoDetalheTemplateView.as_view(),
         name='carrinhodetalhe'),
    path('add/<int:idprod>/', views.CarrinhoAddProdutoView.as_view(),
         name='addcarrinho'),
    path('remover/<int:idprod>/', views.CarrinhoRemoveView.as_view(),
         name='removecarrinho'),
]