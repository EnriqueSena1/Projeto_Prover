from django.core.management.base import BaseCommand
from api.models import CustomUser
from django.contrib.auth.hashers import make_password # Importante para criptografar a senha manualmente

class Command(BaseCommand):
    help = 'Cria o usuario Admin Master usando o formato manual com make_password'

    def handle(self, *args, **options):
        # Dados do Admin
        email = "admin@gmail.com"
        senha = "adm123"
        nome = "Admin Master"
        tipo = "administrador"
        is_adm = True
        
        # Formato solicitado: username igual ao email minusculo
        username = email.lower()

        # Evita duplicidade (Lógica solicitada)
        if CustomUser.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'Usuario "{username}" ja existe. Nenhuma acao necessaria.'))
            return

        self.stdout.write(f'Criando usuario admin: {email}...')

        # Criação do usuário (Formato solicitado)
        # Nota: Adicionei valores padrão para saldo, img e loja para não dar erro no banco
        usuario = CustomUser.objects.create(
            username=username,
            password=make_password(senha), # Criptografa a senha aqui
            email=email,
            first_name=nome,
            nome=nome, # Adicionei esse campo também pois seu model parece usar ele
            is_adm=is_adm,
            tipo=tipo,
            saldo=0.0,  # Valor padrão
            img=None,   # Valor padrão
            is_active=True,
            loja=None   # Admin não tem loja
        )

        self.stdout.write(self.style.SUCCESS(f'Admin criado com sucesso! Login: {username}'))