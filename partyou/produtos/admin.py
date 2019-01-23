from django.contrib import admin

# Register your models here.
from partyou.produtos.models import Produto, Category


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = 'titulo preco'.split()
    ordering = ('titulo',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ['name', 'slug', 'created', 'modified']
    search_fields = ['name', 'slug']
    list_filter = ['created', 'modified']
