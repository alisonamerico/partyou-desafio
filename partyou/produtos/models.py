from django.db import models
from django.urls import reverse


class Category(models.Model):

    name = models.CharField('Nome', max_length=100)
    slug = models.SlugField('Identificador', max_length=100)

    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('produtos:category', kwargs={'slug': self.slug})


class Produto(models.Model):
    titulo = models.CharField(max_length=50)
    slug = models.SlugField('Identificador', max_length=100)
    category = models.ForeignKey('produtos.Category', verbose_name='Categoria', on_delete=models.CASCADE)
    preco = models.DecimalField(decimal_places=2, max_digits=10)
    descricao = models.TextField()
    foto = models.ImageField(upload_to='produtos/', default='http://foo')

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['titulo']

    def __str__(self):
        return self.titulo

    def __repr__(self):
        return f'Produto(titulo={self.titulo!r}, preco={self.preco!r}, descricao={self.descricao!r}'

    def get_absolute_url(self):
        return reverse('produtos:product', kwargs={'slug': self.slug})
