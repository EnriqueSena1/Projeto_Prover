from rest_framework import viewsets
from ..models import *
from ..serializers import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login



class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        senha = request.data.get('senha')
        print('1= ', email, senha)

        # Força os valores para garantir que são strings válidas
        if not email or not senha:
            return Response({'error': 'Email e senha são obrigatórios'}, status=status.HTTP_400_BAD_REQUEST)

        email = str(email).strip().lower()  
        senha = str(senha).strip()
        print("2= ", email, senha)

        user = authenticate(username=email, password=senha)
        print(user)

        if user is not None:
            login(request, user)
            return Response({
                'tipo': user.tipo
            }, status=status.HTTP_200_OK)

        return Response({'error': 'Credenciais inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

class GetDadosUsuarioLogado(APIView):
    def get(self, request):
        usuarioId = request.session.get('_auth_user_id')
        if usuarioId:
            usuario = CustomUser.objects.filter(id= usuarioId).first()
            serializer = CustomUserSerializer(usuario)
            return Response(serializer.data)

        return Response(usuarioId)

class User(APIView):
    def get(self, request, id=None):
        if id:
            usuario = get_object_or_404(CustomUser, pk=id)
            serializer = CustomUserSerializer(usuario)
            return Response(serializer.data, status=status.HTTP_200_OK)

        nome = request.query_params.get("nome")
        if nome:
            usuarios = CustomUser.objects.filter(first_name__icontains=nome)[:5]
        else:
            usuarios = CustomUser.objects.all()[:5]

        serializer = CustomUserSerializer(usuarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        senha = request.data.get('senha')
        first_name = request.data.get('first_name')
        cpf = request.data.get('cpf')
        is_adm = request.data.get('is_adm', False)
        email = request.data.get('email')
        tipo = request.data.get('tipo', 'cliente')
        saldo = request.data.get('saldo', 0.00)

        if not senha or not cpf or not email:
            return Response({"error": "Campos obrigatórios: senha, cpf, email"}, status=status.HTTP_400_BAD_REQUEST)

        username = email.lower()  # ← e-mail vira username

        # Verificações básicas para evitar duplicação
        if CustomUser.objects.filter(username=username).exists():
            return Response({"error": "Email já está em uso como username."}, status=400)
        if CustomUser.objects.filter(cpf=cpf).exists():
            return Response({"error": "CPF já cadastrado."}, status=400)

        usuario = CustomUser.objects.create(
            username=username,
            password=make_password(senha),
            first_name=first_name,
            cpf=cpf,
            is_adm=is_adm,
            email=email,
            tipo=tipo,
            saldo=saldo,
            is_active=True
        )

        return Response({"message": "Usuário criado com sucesso!", "id": usuario.id}, status=status.HTTP_201_CREATED)




    def put(self, request, id):
        usuario = get_object_or_404(CustomUser, pk=id)
        data = request.data.copy()
        operacao = data.get("operacao")

        if operacao in ['adicionar', 'remover']:
            try:
                saldo = int(data.get("saldo", 0))
            except (TypeError, ValueError):
                return Response({"erro": "Saldo inválido."}, status=status.HTTP_400_BAD_REQUEST)

            # Se os campos existirem no modelo CustomUser
            if hasattr(usuario, 'pontuacao') and hasattr(usuario, 'saldo'):
                if operacao == 'adicionar':
                    usuario.pontuacao += saldo
                    usuario.saldo += saldo
                elif operacao == 'remover':
                    if usuario.saldo < saldo:
                        return Response({"erro": "Saldo insuficiente."}, status=status.HTTP_400_BAD_REQUEST)
                    usuario.pontuacao -= saldo
                    usuario.saldo -= saldo

                usuario.save()
                return Response({"message": "Operação realizada com sucesso."}, status=status.HTTP_200_OK)
            else:
                return Response({"erro": "Usuário não possui campos de saldo ou pontuação."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CustomUserSerializer(usuario, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Usuário atualizado com sucesso."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        usuario = get_object_or_404(CustomUser, pk=id)
        usuario.delete()
        return Response({"message": "Usuário deletado com sucesso."}, status=status.HTTP_200_OK)
    

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

class CarrinhoViewSet(viewsets.ModelViewSet):
    queryset = Carrinho.objects.all()
    serializer_class = CarrinhoSerializer

class CompraViewSet(viewsets.ModelViewSet):
    queryset = Compra.objects.all()
    serializer_class = CompraSerializer

class ItensCompraViewSet(viewsets.ModelViewSet):
    queryset = ItensCompra.objects.all()
    serializer_class = ItensCompraSerializer
