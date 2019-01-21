from django.contrib import admin

# Register your models here.
from partyou.produtos.models import Produto


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = 'titulo preco'.split()
    ordering = ('titulo',)
