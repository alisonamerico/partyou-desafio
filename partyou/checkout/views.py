from django.shortcuts import get_object_or_404
from django.views.generic import RedirectView
from django.contrib import messages

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
        return product.get_absolute_url()  # pragma: no cover


create_cartitem = CreateCartItemView.as_view()
