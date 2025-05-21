
from django.views.generic import TemplateView, ListView
from catalogo.models import Produto, Categoria


class IndexView(TemplateView):
    template_name = 'index.html'

class ProdutosListView(ListView):
    model = Produto
    template_name = 'listarprodutos.html'
    context_object_name = 'produtos'
    queryset = Produto.disponiveis.all()

    def get_queryset(self):
        qs = super().get_queryset()
        slugcateg = self.request.GET.get('slugcat')
        if slugcateg:
            try:
                categ = Categoria.objects.get(slug=slugcateg)
                qs = qs.filter(categoria=categ)
            except Categoria.DoesNotExist:
                qs = qs.none()
        return qs  # <-- retorna sempre o queryset, fora do if

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        return context
