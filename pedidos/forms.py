from django import forms
from .models import Pedido

class PedidoModelForm(forms.ModelForm):

    class Meta:
        model = Pedido
        exclude = ['cliente','pago']