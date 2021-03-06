from django.db import models
from django.shortcuts import render, get_object_or_404

from .models import Product, Category
from django.views import generic


class ProductListView(generic.ListView):

    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    paginate_by = 6

    def get_queryset(self):
        queryset = Product.objects.all()  # pragma: no cover
        q = self.request.GET.get('q', '')  # pragma: no cover
        if q:  # pragma: no cover
            queryset = queryset.filter(  # pragma: no cover
                models.Q(name__icontains=q) | models.Q(category__name__icontains=q)
                | models.Q(description__icontains=q)
            )
        return queryset  # pragma: no cover


product_list = ProductListView.as_view()


class CategoryListView(generic.ListView):

    template_name = 'catalog/category.html'
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
        'product': product
    }
    return render(request, 'catalog/product.html', context)
