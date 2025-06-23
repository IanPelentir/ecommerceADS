from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('listaprodutos/',
         views.ProdutosListView.as_view(), name='listtodos'),
    path('listaprodutos/<slug:slugcat>/',
         views.ProdutosListView.as_view(), name='listprods'),
    path('detalheproduto/<slug>/',
         views.ProdutoDetailView.as_view(), name='detalheprod'),
]