from django.contrib.auth.models import AbstractUser
from django.db import models


# Usuário com roles
# models.py

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('cliente', 'Cliente'),
        ('vendedor', 'Vendedor'),
        ('administrador', 'Administrador'),
    ]
    first_name = models.CharField(max_length=150, blank=True, null=True)  # <- adicione isto
    last_name = models.CharField(max_length=150, blank=True, null=True)   # <- adicione isto
    email = models.EmailField(unique=True)
    tipo = models.CharField(max_length=20, choices=ROLE_CHOICES, default='cliente')
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_adm = models.BooleanField(default=False)  
    img =  models.ImageField(upload_to='produtos/', null=True, blank=True)

    # campo exclusivo para vendedores
    loja = models.TextField(max_length=350, blank=True, null=True, verbose_name="loja")

    def __str__(self):
        return f"{self.email} ({self.tipo})"

# Produto
class Produto(models.Model):
    descricao = models.TextField(max_length=350, blank=True, verbose_name="Descrição")
    valor = models.DecimalField(max_digits=8, decimal_places=2)
    validade = models.DateField(verbose_name="Validade", blank=True, null=True)
    quantidade = models.PositiveIntegerField(verbose_name="Quantidade", default=0)
    tipo_produto = models.CharField(max_length=100, verbose_name="Tipo de Embalagem", default='Outro')
    classe = models.CharField(max_length=100, verbose_name="Classificação",  default="Alimento")
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True, verbose_name="Imagem do Produto")

    def __str__(self):
        return self.descricao

# Carrinho
class Carrinho(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    qtd_carrinho = models.PositiveIntegerField()
    valor_carrinho = models.DecimalField(max_digits=8, decimal_places=2)

# Compra
class Compra(models.Model):
    STATUS_CHOICES = [
        ("Pendente", "Pendente"),
        ("Concluido", "Concluído"),
    ]

    total = models.DecimalField(max_digits=10, decimal_places=2)
    pedido = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pendente')
    data_compra = models.DateTimeField(auto_now_add=True)
    cliente = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='compras_cliente', null=True)

    vendedor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='compras_vendedor')

# Itens da Compra
class ItensCompra(models.Model):
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE)
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, null=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
