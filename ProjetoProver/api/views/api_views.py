from rest_framework import viewsets
from rest_framework.views import APIView
from ..models import *
from ..serializers import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password

from ..models import CustomUser
from ..serializers import CustomUserSerializer

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
        username = request.data.get('username')
        senha = request.data.get('senha')
        first_name = request.data.get('first_name')
        cpf = request.data.get('cpf')
        is_adm = request.data.get('is_adm', False)

        if not username or not senha or not cpf:
            return Response({"error": "Campos obrigatórios: username, senha, cpf"}, status=status.HTTP_400_BAD_REQUEST)

        usuario = CustomUser.objects.create(
            username=username,
            password=make_password(senha),
            first_name=first_name,
            cpf=cpf,
            is_adm=is_adm,
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

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

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
