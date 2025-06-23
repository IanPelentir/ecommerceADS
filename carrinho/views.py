from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, TemplateView

from carrinho.car import Carrinho
from catalogo.models import Produto
from .forms import CarrinhoAddProdForm


class CarrinhoAddProdutoView(FormView):
    form_class = CarrinhoAddProdForm
    success_url = reverse_lazy('listtodos')

    def post(self, request, *args, **kwargs):
        self.produto = Produto.objects.get(id=kwargs['idprod'])
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        cd = form.cleaned_data
        carrinho = Carrinho(self.request)
        carrinho.addProduto(produto=self.produto, quant=cd['quant'],
                            alterarquant=cd['alterar'])
        return super().form_valid(form)

    def form_invalid(self, form):
        return redirect('listtodos')


class CarrinhoRemoveView(View):

    def post(self, request, *args, **kwargs):
        self.produto = Produto.objects.get(id=kwargs['idprod'])
        carrinho = Carrinho(request)
        carrinho.removerProduto(self.produto)
        return redirect('carrinhodetalhe')


class CarrinhoDetalheTemplateView(TemplateView):
    template_name = 'carrinho/detalhe.html'

    def get_context_data(self, **kwargs):
        cont = super().get_context_data(**kwargs)
        carrinho = Carrinho(self.request)
        for item in carrinho:
            item['alterar'] = CarrinhoAddProdForm(initial={
                                                   'quant':item['quantidade'],
                                                   'alterar':True
                                                 })
        cont['carrinho'] = carrinho
        return cont