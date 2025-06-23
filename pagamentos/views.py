from django.shortcuts import get_object_or_404, redirect, reverse

from ecommerce import settings
from pedidos.models import Pedido
from django.views.generic import FormView, TemplateView

import braintree
from .forms import CheckoutForm


class ProcessarPagamentoView(FormView):
    """
    View para permitir que o usuário realize o pagamento de um pedido
    """
    form_class = CheckoutForm
    template_name = 'pagamento/processar.html'

    def dispatch(self, request, *args, **kwargs):
        braintree_env = braintree.Environment.Sandbox
        # Configurando Braintree
        braintree.Configuration.configure(
            braintree_env,
            merchant_id=settings.BRAINTREE_MERCHANT_ID,
            public_key=settings.BRAINTREE_PUBLIC_KEY,
            private_key=settings.BRAINTREE_PRIVATE_KEY,
        )
        self.pedido = Pedido.objects.get(id=request.GET.get('idpedido'))
        self.braintree_client_token = braintree.ClientToken.generate({})
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        cont = super().get_context_data(**kwargs)
        cont['braintree_client_token'] = self.braintree_client_token
        return cont

    def form_valid(self, form):
        valor_total = self.pedido.get_total_geral()
        result = braintree.Transaction.sale({
            'amount': valor_total,
            'payment_method_nonce': form.cleaned_data['payment_method_nonce'],
            'options': {
                'submit_for_settlement': True,
            }
        })
        if not result.is_success:
            cont = self.get_context_data()
            cont['form'] = self.get_form(self.get_form_class())
            cont['braintree_error'] = 'Pagamento não processado!'
            return self.render_to_response(cont)
        transaction_id = result.transaction.id
        self.pedido.pago = True
        self.pedido.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('pgto_realizado')


class PagamentoRealizadoView(TemplateView):
    template_name = 'pagamento/realizado.html'


class PagamentoCanceladoView(TemplateView):
    template_name = 'pagamento/cancelado.html'
