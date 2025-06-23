import os.path

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
    slug = instance.slug
    ext = os.path.splitext(filename)[1]
    caminho = f'produtos/{slug}{ext}'
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