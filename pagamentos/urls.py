from django.urls import path
from .views import ProcessarPagamentoView, PagamentoCanceladoView, PagamentoRealizadoView

urlpatterns = [
    path('processar/', ProcessarPagamentoView.as_view(),
         name='processarpgt'),
    path('realizado/', PagamentoRealizadoView.as_view(),
         name='realizado'),
    path('cancelado/', PagamentoCanceladoView.as_view(),
         name='cancelado'),
]