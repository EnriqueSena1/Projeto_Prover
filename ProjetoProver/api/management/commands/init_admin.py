from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Cria o usuario Admin Master automaticamente se nao existir'

    def handle(self, *args, **options):
        User = get_user_model()
        email = "admin@gmail.com"
        senha = "adm123"

        if not User.objects.filter(email=email).exists():
            self.stdout.write(f'Criando usuario admin: {email}...')
            
            # Cria o superusuario (que ja cuida da senha criptografada)
            usuario = User.objects.create_superuser(
                email=email,
                password=senha
            )
            
            # Define os campos personalizados que voce pediu
            usuario.nome = "Admin Master"
            usuario.tipo = "administrador"
            usuario.is_adm = True
            
            usuario.save()
            
            self.stdout.write(self.style.SUCCESS(f'Admin criado com sucesso! Email: {email} / Senha: {senha}'))
        else:
            self.stdout.write(self.style.WARNING('Usuario admin ja existe. Nenhuma acao necessaria.'))