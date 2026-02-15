from django.core.management.base import BaseCommand
from api.models import CustomUser

class Command(BaseCommand):
    help = 'Cria o usuario Admin Master e um Colaborador padrão no banco de dados'

    def handle(self, *args, **options):
        # =========================
        # ADMIN MASTER
        # =========================
        email_admin = "admin@gmail.com"
        senha_admin = "adm123"

        if not CustomUser.objects.filter(email=email_admin).exists():
            self.stdout.write(f'Criando usuario Admin: {email_admin}...')

            admin = CustomUser.objects.create_user(
                username=email_admin,
                email=email_admin,
                password=senha_admin,
                first_name="Admin Master",
                is_adm=True,
                tipo="administrador",
                is_active=True,
            )
            admin.save()

            self.stdout.write(self.style.SUCCESS(
                f'Admin Master criado! Login: {email_admin}'
            ))
        else:
            self.stdout.write(self.style.WARNING(
                f'Usuario {email_admin} ja existe.'
            ))

        # =========================
        # COLABORADOR
        # =========================
        email_colaborador = "colaborador01@gmail.com"
        senha_colaborador = "user1234"

        if not CustomUser.objects.filter(email=email_colaborador).exists():
            self.stdout.write(f'Criando usuario Colaborador: {email_colaborador}...')

            colaborador = CustomUser.objects.create_user(
                username=email_colaborador,
                email=email_colaborador,
                password=senha_colaborador,
                first_name="administrador",
                is_adm=True,
                tipo="administrador",
                is_active=True,
            )
            colaborador.save()

            self.stdout.write(self.style.SUCCESS(
                f'Colaborador criado! Login: {email_colaborador}'
            ))
        else:
            self.stdout.write(self.style.WARNING(
                f'Usuario {email_colaborador} ja existe.'
            ))





# from django.core.management.base import BaseCommand
# from api.models import CustomUser  # <--- Importando diretamente o seu modelo

# class Command(BaseCommand):
#     help = 'Cria o usuario Admin Master personalizado no banco de dados'

#     def handle(self, *args, **options):
#         # Dados do Admin
#         email_admin = "admin@gmail.com"
#         senha_admin = "adm123"
        
#         # Verifica se existe olhando direto na tabela do CustomUser
#         if not CustomUser.objects.filter(email=email_admin).exists():
#             self.stdout.write(f'Criando usuario personalizado: {email_admin}...')
            
#             # Usamos create_user para criptografar a senha corretamente
#             usuario = CustomUser.objects.create_user(
#                 username=email_admin,
#                 email=email_admin,
#                 password=senha_admin,
#                 first_name="Admin Master",
#                 is_adm=True,
#                 tipo="administrador",
#                 is_active=True,
#             )
            
#             # Salva o admin no banco
#             usuario.save()
            
#             self.stdout.write(self.style.SUCCESS(f'Admin Master criado! Login: {email_admin}'))
#         else:
#             self.stdout.write(self.style.WARNING(f'Usuario {email_admin} ja existe.'))