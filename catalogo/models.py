import os
from datetime import datetime
from django.db import models


class ProdDisponiveisManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(disponivel=True)


class Categoria(models.Model):
    nome = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ('nome',)

    def __str__(self):
        return self.nome


def get_upload_path(instance, filename):
    # Usa a data atual no formato YYYY-MM-DD para criar subpasta
    data_hoje = datetime.now().strftime('%Y-%m-%d')
    ext = os.path.splitext(filename)[1]  # pega extensão do arquivo, ex: .jpg, .png
    # nome do arquivo = slug + extensão
    nome_arquivo = f'{instance.slug}{ext}'
    # caminho completo dentro da pasta media
    caminho = f'produtos/{data_hoje}/{nome_arquivo}'
    return caminho


class Produto(models.Model):
    objects = models.Manager()
    disponiveis = ProdDisponiveisManager()
    nome = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey('Categoria',
                                  on_delete=models.CASCADE,
                                  related_name='produtos')
    imagem = models.ImageField(upload_to=get_upload_path,
                               blank=True)
    disponivel = models.BooleanField(default=True)
    criado = models.DateTimeField(auto_now_add=True)
    atualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ('categoria', 'nome', )

    def __str__(self):
        return self.nome
