from django.db import models

from partyou.catalog.models import Product


class CartItemManager(models.Manager):

    def add_item(self, cart_key, product):
        if self.filter(cart_key=cart_key, product=product).exists():  # pragma: no cover
            created = False  # pragma: no cover
            cart_item = self.get(cart_key=cart_key, product=product)  # pragma: no cover
            cart_item.quantity = cart_item.quantity + 1  # pragma: no cover
            cart_item.save()  # pragma: no cover
        else:
            created = True  # pragma: no cover
            cart_item = CartItem.objects.create(  # pragma: no cover
                cart_key=cart_key, product=product, price=product.price
            )
        return cart_item, created  # pragma: no cover


class CartItem(models.Model):

    cart_key = models.CharField(
        'Chave do Carrinho', max_length=40, db_index=True
    )
    product = models.ForeignKey(Product, verbose_name='Produto', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('Quantidade', default=1)
    price = models.DecimalField('Preço', decimal_places=2, max_digits=8)

    objects = CartItemManager()

    class Meta:
        verbose_name = 'Item do Carrinho'
        verbose_name_plural = 'Itens dos Carrinhos'
        unique_together = (('cart_key', 'product'),)

    def __str__(self):
        return '{} [{}]'.format(self.product, self.quantity)  # pragma: no cover


def post_save_cart_item(instance, **kwargs):
    if instance.quantity < 1:  # pragma: no cover
        instance.delete()  # pragma: no cover


models.signals.post_save.connect(post_save_cart_item, sender=CartItem, dispatch_uid='post_save_cart_item')
