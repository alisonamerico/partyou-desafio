from django.db import models
from django.conf import settings

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


class OrderManager(models.Manager):

    def create_order(self, user, cart_items):
        order = self.create(user=user)  # pragma: no cover
        for cart_item in cart_items:  # pragma: no cover
            order_item = OrderItem.objects.create(  # noqa  # pragma: no cover
                order=order, quantity=cart_item.quantity, product=cart_item.product,
                price=cart_item.price
            )
        return order  # pragma: no cover


class Order(models.Model):

    STATUS_CHOICES = (
        (0, 'Aguardando Pagamento'),
        (1, 'Concluída'),
        (2, 'Cancelada'),
    )

    PAYMENT_OPTION_CHOICES = (
        ('deposit', 'Depósito'),
        ('pagseguro', 'PagSeguro'),
        ('paypal', 'Paypal'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuário', on_delete=models.CASCADE)
    status = models.IntegerField(
        'Situação', choices=STATUS_CHOICES, default=0, blank=True
    )
    payment_option = models.CharField(
        'Opção de Pagamento', choices=PAYMENT_OPTION_CHOICES, max_length=20,
        default='deposit'
    )

    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)

    objects = OrderManager()

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    def __str__(self):
        return 'Pedido #{}'.format(self.pk)  # pragma: no cover

    def products(self):
        products_ids = self.items.values_list('product')  # pragma: no cover
        return Product.objects.filter(pk__in=products_ids)  # pragma: no cover

    def total(self):
        aggregate_queryset = self.items.aggregate(  # pragma: no cover
            total=models.Sum(
                models.F('price') * models.F('quantity'),
                output_field=models.DecimalField()
            )
        )
        return aggregate_queryset['total']  # pragma: no cover


class OrderItem(models.Model):

    order = models.ForeignKey(Order, verbose_name='Pedido', related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Produto', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('Quantidade', default=1)
    price = models.DecimalField('Preço', decimal_places=2, max_digits=8)

    class Meta:
        verbose_name = 'Item do pedido'
        verbose_name_plural = 'Itens dos pedidos'

    def __str__(self):
        return '[{}] {}'.format(self.order, self.product)


def post_save_cart_item(instance, **kwargs):
    if instance.quantity < 1:  # pragma: no cover
        instance.delete()  # pragma: no cover


models.signals.post_save.connect(post_save_cart_item, sender=CartItem, dispatch_uid='post_save_cart_item')
