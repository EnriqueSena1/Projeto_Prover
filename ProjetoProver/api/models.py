from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser

# Usuário personalizado
class CustomUser(AbstractUser):
    is_adm = models.BooleanField(default=False)
    cpf = models.CharField(max_length=11, null=False, blank=False, unique=True)

# Cliente
class Cliente(models.Model):
    nome = models.CharField(max_length=50, null=False, blank=False)
    cpf = models.CharField(max_length=11, null=False, blank=False, unique=True)
    telefone = models.CharField(max_length=11, null=False, blank=False)

    def __str__(self):
        return self.nome

# Produto
class Produto(models.Model):
    tipo_choices = [
        ("Perecivel", "Perecível"),
        ("Congelado", "Congelado"),
        ("Nao_Perecivel", "Não Perecível"),
    ]

    nome = models.CharField(max_length=50, null=False, blank=False)
    marca = models.CharField(max_length=50, null=False, blank=False)
    qtd_prod = models.PositiveIntegerField(null=False, blank=False)
    valor = models.DecimalField(max_digits=8, decimal_places=2, null=False, blank=False)
    tipo_prod = models.CharField(max_length=16, choices=tipo_choices)
    descricao_pro = models.TextField(max_length=350, blank=True)
    img_prod = models.CharField(max_length=150, null=False, blank=False)

    def __str__(self):
        return self.nome

# Carrinho
class Carrinho(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    qtd_carrinho = models.PositiveIntegerField(null=False, blank=False)
    valor_carrinho = models.DecimalField(max_digits=8, decimal_places=2, null=False, blank=False)

# Compra
class Compra(models.Model):
    status_pedidos = [
        ("Pendente", "Pendente"),
        ("Concluido", "Concluído"),
    ]

    total = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    pedido = models.CharField(max_length=10, choices=status_pedidos, default='Pendente')
    data_compra = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comprador')
    vendedor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='vendedor')

# Itens da Compra
class ItensCompra(models.Model):
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE)
    vendedor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)

# Funcionario (baseado na imagem)
class Funcionario(models.Model):
    nome = models.CharField(max_length=255, null=False, blank=False)
    sobrenome = models.CharField(max_length=255, null=False, blank=False)
    cpf = models.CharField(max_length=14, null=False, blank=False, unique=True)
    tempo_de_servico = models.IntegerField(default=0, null=False, blank=False)
    remuneracao = models.DecimalField(max_digits=8, decimal_places=2, null=False, blank=False)

    def __str__(self):
        return f"{self.nome} {self.sobrenome}"

