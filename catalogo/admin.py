from django.contrib import admin
from .models import Categoria, Produto


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'slug']
    prepopulated_fields = {'slug':('nome',)}

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['categoria', 'nome', 'slug',
                    'preco', 'disponivel', 'criado', 'atualizado']
    list_filter = ['disponivel', 'criado', 'atualizado']
    prepopulated_fields = {'slug':('nome',)}
    list_editable = ['preco', 'disponivel']

