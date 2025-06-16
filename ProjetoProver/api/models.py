from django.contrib.auth.models import AbstractUser
from django.utils import timezone
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
    is_disponivel = models.BooleanField(default=True, verbose_name="Disponível para Carrinho")

    exibir_no_carrinho = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        hoje = timezone.now().date()
        if self.quantidade <= 0 or (self.validade and self.validade < hoje):
            self.is_disponivel = False
        else:
            self.is_disponivel = True
        super().save(*args, **kwargs)  

    def __str__(self):
        return self.descricao



# compra
class Compra(models.Model):
    cliente = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="compras", null=True)
    data = models.DateTimeField(auto_now_add=True)
    total_itens = models.PositiveIntegerField(default=0)
    total_preco = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Compra de {self.cliente.username} em {self.data.strftime('%d/%m/%Y')}"

class ItemCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name='itens_compra')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)




    def __str__(self):
        return f'{self.quantidade} de {self.produto.descricao} em Compra {self.compra.id}'

