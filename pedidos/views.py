from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, ListView

from carrinho.car import Carrinho
from .forms import PedidoModelForm
from .models import Pedido, ItensPedido

class PedidoCreateView(LoginRequiredMixin, CreateView):
    form_class = PedidoModelForm
    template_name = 'pedido/novopedido.html'
    # success_url = reverse_lazy('resumopedido')

    def form_valid(self, form):
        car = Carrinho(self.request)
        pedido = form.save(commit=False)
        us = self.request.user
        pedido.cliente = us
        pedido.save()
        for item in car:
            ItensPedido.objects.create(pedido=pedido,
                                       produto=item['produto'],
                                       preco_unit=item['preco'],
                                       quantidade=item['quantidade'])
        car.limpar_carrinho()
        self.request.session['idpedido'] = pedido.id
        return redirect('resumopedido', pedido.id)


class ResumoPedidoTemplateView(TemplateView):
    template_name = 'pedido/resumopedido.html'

    def get_context_data(self, **kwargs):
        ct = super().get_context_data(**kwargs)
        ct['pedido'] = Pedido.objects.get(id=self.kwargs['idpedido'])
        return ct

class PedidosListView(LoginRequiredMixin, ListView):
    template_name = 'pedido/meuspedidos.html'
    model = Pedido
    context_object_name = 'pedidos'


    def get_queryset(self):
        return Pedido.objects.filter(cliente=self.request.user)