from django.core.management.base import BaseCommand
from api.models import CustomUser  # <--- Importando diretamente o seu modelo

class Command(BaseCommand):
    help = 'Cria o usuario Admin Master personalizado no banco de dados'

    def handle(self, *args, **options):
        # Dados do Admin
        email_admin = "admin@gmail.com"
        senha_admin = "adm123"
        
        # Username interno (obrigatório pelo Django, mesmo usando login por email)
        username_interno = "admin_master_system" 

        # Verifica se existe olhando direto na tabela do CustomUser
        if not CustomUser.objects.filter(email=email_admin).exists():
            self.stdout.write(f'Criando usuario personalizado: {email_admin}...')
            
            # Usamos create_user para criptografar a senha corretamente
            usuario = CustomUser.objects.create_user(
                username=username_interno,
                email=email_admin,
                password=senha_admin
            )
            
            # Define seus campos personalizados
            usuario.nome = "Admin Master"
            usuario.tipo = "administrador"
            usuario.is_adm = True
            
            # Configurações de acesso (opcional, ajustado para o seu caso)
            usuario.is_superuser = False
            usuario.is_staff = False
            
            usuario.save()
            
            self.stdout.write(self.style.SUCCESS(f'Admin Master criado! Login: {email_admin}'))
        else:
            self.stdout.write(self.style.WARNING(f'Usuario {email_admin} ja existe.'))