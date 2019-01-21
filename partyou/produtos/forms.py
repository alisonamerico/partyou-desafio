from django import forms

from partyou.produtos.models import Produto


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = 'titulo preco descricao foto'.split()
