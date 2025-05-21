from django.urls import path
from .views import IndexView, ProdutosListView

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('produtos/', ProdutosListView.as_view(), name='produtos-lista'),
]
