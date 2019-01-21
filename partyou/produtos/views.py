from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
# Create your views here.
from django.urls import reverse

from partyou.produtos.forms import ProdutoForm
from partyou.produtos.models import Produto


def index(request):
    query_set = Produto.objects.order_by('titulo')
    ctx = {
        'produtos': list(query_set)
    }

    return render(request, 'produtos/index.html', context=ctx)


@login_required
def new(request):
    ctx = {'form': ProdutoForm()}
    return render(request, 'produtos/produto_form.html', context=ctx)


@login_required
def create(request):
    # Extraia os dados do request
    form = ProdutoForm(request.POST, request.FILES)
    # Valide os Inputs
    if not form.is_valid():
        ctx = {'form': form}
        return render(request, 'produtos/produto_form.html', context=ctx, status=400)
    # Se válido, salve no banco e redirecione
    form.save()
    return redirect(reverse('produtos:index'))
