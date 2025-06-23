from decimal import Decimal

from django.conf import settings

from catalogo.models import Produto

class Carrinho(object):

    def __init__(self, request):
        """
        Inicializa o carrinho de compras
        :param request: a requisição https
        """
        self.session = request.session
        carrinho = self.session.get(settings.CART_SESSION_ID)
        if not carrinho:
            carrinho = self.session[settings.CART_SESSION_ID] = {}
        self.carrinho = carrinho

    def addProduto(self, produto, quant=1, alterarquant=False):
        """
        Adiciona um item ao carrinho de compras ou atualiza sua
        quantidade
        :param produto: o item de um determinado produto
        :param quant: a quantidade de produtos
        :param alterarquant: quando necessário alterar a quantidade de
                             itens do produto
        :return: sem retorno
        """
        idprod = str(produto.id)
        if idprod not in self.carrinho:
            self.carrinho[idprod] = {'quantidade':0,
                                     'preco':str(produto.preco)}
        if alterarquant:
            self.carrinho[idprod]['quantidade'] = quant
        else:
            self.carrinho[idprod]['quantidade'] += quant
        self._salvar()

    def _salvar(self):
        self.session.modified = True

    def removerProduto(self,  produto):
        """
        Remove um item do carrinho de compras
        :param produto: o produto a ser removido
        :return: sem retorno
        """
        idprod = str(produto.id)
        if idprod in self.carrinho:
            del self.carrinho[idprod]
            self._salvar()

    def __iter__(self):
        """
        percorre os itens do carrinho e obtem informações importantes
        :return: as informações dos itens do carrinho
        """
        idsprodutos = self.carrinho.keys()
        produtos  = Produto.objects.filter(id__in=idsprodutos)
        carrinho = self.carrinho.copy()
        for p in produtos:
            carrinho[str(p.id)]['produto'] = p
        for item in carrinho.values():
            item['preco'] = Decimal(item['preco'])
            item['preco_total'] = item['preco'] * item['quantidade']
            yield item

    def __len__(self):
        """
        Soma a quantidade de itens no carrinho
        :return: Quantos itens tem no carrinho
        """
        return sum(item['quantidade'] for item in self.carrinho.values())

    def get_preco_total(self):
        return sum(Decimal(item['preco'] * item['quantidade'])
                   for item in self.carrinho.values())

    def limpar_carrinho(self):
        del self.session[settings.CART_SESSION_ID]
        self._salvar()