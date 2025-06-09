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

    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=11, unique=True)
    tipo = models.CharField(max_length=20, choices=ROLE_CHOICES, default='cliente')
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    is_adm = models.BooleanField(default=False)  
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} - {self.email} ({self.tipo})"

# Produto
class Produto(models.Model):
    TIPO_CHOICES = [
        ("Perecivel", "Perecível"),
        ("Congelado", "Congelado"),
        ("Nao_Perecivel", "Não Perecível"),
    ]

    nome = models.CharField(max_length=50)
    marca = models.CharField(max_length=50)
    qtd_prod = models.PositiveIntegerField()
    valor = models.DecimalField(max_digits=8, decimal_places=2)
    tipo_prod = models.CharField(max_length=16, choices=TIPO_CHOICES)
    descricao_pro = models.TextField(max_length=350, blank=True)
    img_prod = models.CharField(max_length=150)

    def __str__(self):
        return self.nome

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
