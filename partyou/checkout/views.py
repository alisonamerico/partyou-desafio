from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import RedirectView, TemplateView
from django.contrib import messages
from django.forms import modelformset_factory

from partyou.catalog.models import Product

from partyou.checkout.models import CartItem


class CreateCartItemView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        product = get_object_or_404(Product, slug=self.kwargs['slug'])  # pragma: no cover
        if self.request.session.session_key is None:  # pragma: no cover
            self.request.session.save()  # pragma: no cover
        cart_item, created = CartItem.objects.add_item(  # pragma: no cover
                self.request.session.session_key, product
        )
        if created:  # pragma: no cover
            messages.success(self.request, 'Produto adicionado com sucesso')  # pragma: no cover
        else:
            messages.success(self.request, 'Produto atualizado com sucesso')  # pragma: no cover
        return reverse('checkout:cart_item')  # pragma: no cover


create_cartitem = CreateCartItemView.as_view()


class CartItemView(TemplateView):

    template_name = 'checkout/cart.html'

    def get_formset(self, clear=False):
        CartItemFormSet = modelformset_factory(  # pragma: no cover
            CartItem, fields=('quantity',), can_delete=True, extra=0
        )
        session_key = self.request.session.session_key  # pragma: no cover
        if session_key:  # pragma: no cover
            if clear:  # pragma: no cover
                formset = CartItemFormSet(  # pragma: no cover
                    queryset=CartItem.objects.filter(cart_key=session_key)
                )
            else:
                formset = CartItemFormSet(  # pragma: no cover
                    queryset=CartItem.objects.filter(cart_key=session_key), data=self.request.POST or None
                )
        else:
            formset = CartItemFormSet(  # pragma: no cover
                queryset=CartItem.objects.none())
        return formset  # pragma: no cover

    def get_context_data(self, **kwargs):
        context = super(CartItemView, self).get_context_data(**kwargs)  # pragma: no cover
        context['formset'] = self.get_formset()  # pragma: no cover
        return context  # pragma: no cover

    def post(self, request, *args, **kwargs):
        formset = self.get_formset()  # pragma: no cover
        context = self.get_context_data(**kwargs)  # pragma: no cover
        if formset.is_valid():  # pragma: no cover
            formset.save()  # pragma: no cover
            messages.success(request, 'Carrinho atualizado com sucesso')  # pragma: no cover
            context['formset'] = self.get_formset(clear=True)  # pragma: no cover
        return self.render_to_response(context)  # pragma: no cover


cart_item = CartItemView.as_view()
