from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView

from carrinho.forms import CarrinhoAddProdForm
from .models import Produto, Categoria


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        cont = super().get_context_data(**kwargs)
        cont['prods'] = Produto.disponiveis.all().order_by('?')[:3]
        return cont


class ProdutosListView(ListView):
    model = Produto
    template_name = 'produtos/listarprodutos.html'
    context_object_name = 'produtos'
    queryset = Produto.disponiveis.all()

    def get_queryset(self):
        qs = super().get_queryset()
        if self.kwargs and self.kwargs['slugcat']:
            slugcateg = self.kwargs['slugcat']
            categ = Categoria.objects.get(slug=slugcateg)
            qs = qs.filter(categoria=categ)
        return qs

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['categs'] = Categoria.objects.all()
        if self.kwargs and self.kwargs['slugcat']:
            slug = self.kwargs['slugcat']
            cat = contexto['categs'].get(slug=slug)
            contexto['cat'] = cat
        return contexto


class ProdutoDetailView(DetailView):
    model = Produto
    template_name = "produtos/detalheproduto.html"

    def get_context_data(self, **kwargs):
        cont = super().get_context_data(**kwargs)
        formadd = CarrinhoAddProdForm()
        cont['formadd'] = formadd
        return cont

