from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import Product, Category


class ProductListView(generic.ListView):

    model = Product
    template_name = 'produtos/product_list.html'
    # context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        return context

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
