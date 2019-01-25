# from django.contrib.auth.decorators import login_required
# from django.shortcuts import redirect, render
# # Create your views here.
# from django.urls import reverse
#
# from partyou.produtos.forms import ProdutoForm
# from partyou.produtos.models import Produto
#
#
# def index(request):
#     query_set = Produto.objects.order_by('titulo')
#     ctx = {
#         'produtos': list(query_set)
#     }
#
#     return render(request, 'produtos/index.html', context=ctx)
#
#
# @login_required
# def create_product(request):
#     ctx = {'form': ProdutoForm()}
#     return render(request, 'produtos/produto_form.html', context=ctx)
#
#
# @login_required
# def create(request):
#     # Extraia os dados do request
#     form = ProdutoForm(request.POST, request.FILES)
#     # Valide os Inputs
#     if not form.is_valid():
#         ctx = {'form': form}
#         return render(request, 'produtos/produto_form.html', context=ctx, status=400)
#     # Se válido, salve no banco e redirecione
#     form.save()
#     return redirect(reverse('produtos:list_product'))


from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import Product, Category


class ProductListView(generic.ListView):

    model = Product
    template_name = 'produtos/product_list.html'
    context_object_name = 'products'
    paginate_by = 3


product_list = ProductListView.as_view()


class CategoryListView(generic.ListView):

    template_name = 'produtos/category.html'
    context_object_name = 'product_list'
    paginate_by = 3

    def get_queryset(self):
        return Product.objects.filter(category__slug=self.kwargs['slug'])  # pragma: no cover

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)  # pragma: no cover
        context['current_category'] = get_object_or_404(Category, slug=self.kwargs['slug'])  # pragma: no cover
        return context  # pragma: no cover


category = CategoryListView.as_view()


def product(request, slug):
    product = Product.objects.get(slug=slug)  # pragma: no cover
    context = {  # pragma: no cover
        'product': product  # pragma: no cover
    }
    return render(request, 'produtos/product.html', context)  # pragma: no cover
