from rest_framework import viewsets
from ..models import *
from ..serializers import *
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from rest_framework.permissions import IsAuthenticated


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
        if request.user.is_authenticated:
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
        
        else:
            return redirect('/login/')
        
    def post(self, request):
        # 🚀 LIBERA APENAS SE NÃO EXISTIR ADMIN AINDA
        existe_admin = CustomUser.objects.filter(is_adm=True).exists()

        if existe_admin and not request.user.is_authenticated:
            return Response(
                {"error": "Login necessário"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Dados obrigatórios
        nome = request.data.get('nome')
        email = request.data.get('email')
        senha = request.data.get('senha')

        if not nome or not email or not senha:
            return Response(
                {"error": "Campos obrigatórios: nome, email, senha"},
                status=status.HTTP_400_BAD_REQUEST
            )

        email = email.lower().strip()

        if CustomUser.objects.filter(username=email).exists():
            return Response(
                {"error": "Email já cadastrado"},
                status=status.HTTP_400_BAD_REQUEST
            )

        usuario = CustomUser.objects.create(
            username=email,
            password=make_password(senha),
            email=email,
            first_name=nome,
            tipo='administrador',
            is_adm=True,
            is_active=True
        )

        return Response(
            {
                "message": "Administrador criado com sucesso",
                "id": usuario.id
            },
            status=status.HTTP_201_CREATED
        )


    # def post(self, request):
    #     if request.user.is_authenticated:

    #         # Dados obrigatórios
    #         nome = request.data.get('nome')# ← usado como first_name
    #         email = request.data.get('email')
    #         senha = request.data.get('senha')

    #         # Dados opcionais
    #         is_adm = request.data.get('is_adm', False)
    #         tipo = request.data.get('tipo', 'cliente')
    #         saldo = request.data.get('saldo', 0.00)
    #         imagem = request.FILES.get('img')  
    #         loja = request.data.get('loja')  

    #         # Validação básica
    #         if not email or not senha or not nome:
    #             return Response(
    #                 {"error": "Campos obrigatórios: nome, email, senha"},
    #                 status=status.HTTP_400_BAD_REQUEST
    #             )

    #         username = email.lower()

    #         # Evita duplicidade
    #         if CustomUser.objects.filter(username=username).exists():
    #             return Response({"error": "Email já está em uso."}, status=400)

    #         # Criação do usuário
    #         usuario = CustomUser.objects.create(
    #             username=username,
    #             password=make_password(senha),
    #             email=email,
    #             first_name=nome,
    #             is_adm=is_adm,
    #             tipo=tipo,
    #             saldo=saldo,
    #             img=imagem,
    #             is_active=True,
    #             loja=loja if tipo == 'vendedor' else None  
    #         )
            
    #         return Response(
    #             {"message": "Usuário criado com sucesso!", "id": usuario.id},
    #             status=status.HTTP_201_CREATED
    #         )

    #     else:
    #         return redirect('/login/')


    def put(self, request, id):
        if request.user.is_authenticated:
            usuario = get_object_or_404(CustomUser, pk=id)
            data = request.data.copy()
            operacao = data.get("operacao")

                # Operações específicas de saldo
            if operacao in ['adicionar', 'remover']:
                try:
                    valor_saldo = float(data.get("saldo", 0))
                except (TypeError, ValueError):
                    return Response({"erro": "Valor de saldo inválido."}, status=status.HTTP_400_BAD_REQUEST)

                if operacao == 'adicionar':
                    usuario.saldo += valor_saldo
                elif operacao == 'remover':
                    if usuario.saldo < valor_saldo:
                        return Response({"erro": "Saldo insuficiente."}, status=status.HTTP_400_BAD_REQUEST)
                    usuario.saldo -= valor_saldo

                usuario.save()
                return Response({
                    "message": f"Saldo {operacao} com sucesso.", 
                    "novo_saldo": float(usuario.saldo)
                }, status=status.HTTP_200_OK)

            
            if 'operacao' in data:
                del data['operacao']

                # Tratamento especial para senha
            if 'senha' in data and data['senha']:
                data['password'] = make_password(data['senha'])
                del data['senha']

            # Tratamento especial para nome (mapear para first_name)
            if 'nome' in data:
                data['first_name'] = data['nome']
                del data['nome']

            # Tratamento especial para email (atualizar username também)
            if 'email' in data:
                email = data['email'].lower().strip()
                    # Verificar se o email já existe em outro usuário
                if CustomUser.objects.filter(email=email).exclude(id=id).exists():
                    return Response({"erro": "Este email já está em uso por outro usuário."}, status=status.HTTP_400_BAD_REQUEST)
                data['email'] = email
                data['username'] = email

            # Tratamento para imagem
            if 'img' in request.FILES:
                data['img'] = request.FILES['img']

            # Tratamento para loja (somente se for vendedor)
            if 'loja' in data:
                if usuario.tipo == 'vendedor':
                    data['loja'] = data['loja']
                else:
                    data['loja'] = None 

            # Usar o serializer para validação e atualização
            serializer = CustomUserSerializer(usuario, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message": "Usuário atualizado com sucesso.",
                    "usuario": serializer.data
                }, status=status.HTTP_200_OK)

            return Response({
                "erro": "Dados inválidos.",
                "detalhes": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return redirect('/login/')

    def delete(self, request, id):
        if request.user.is_authenticated:
            usuario = get_object_or_404(CustomUser, pk=id)
            usuario.delete()
            return Response({"message": "Usuário deletado com sucesso."}, status=status.HTTP_200_OK)
        else:
            return redirect('/login/')
    

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]  # só logado pode acessar


class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    permission_classes = [IsAuthenticated]  # só logado pode acessar


class CompraViewSet(viewsets.ModelViewSet):
    queryset = Compra.objects.all()
    serializer_class = CompraSerializer
    permission_classes = [IsAuthenticated]  # só logado pode acessar




class CompraCreateAPIView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            data = request.data

            try:
                with transaction.atomic():
                    cliente = CustomUser.objects.get(id=data["cliente_id"])
                    total_preco = Decimal(str(data["total_preco"])) 
                    itens_data = data["itens"]
                    
                    # Verifica saldo do cliente
                    if cliente.saldo < total_preco:
                        raise ValueError("Saldo insuficiente para realizar a compra.")

                    # Debita o saldo do cliente
                    cliente.saldo -= total_preco
                    cliente.save()

                    # Cria a compra
                    compra = Compra.objects.create(
                        cliente=cliente,
                        total_itens=len(itens_data),
                        total_preco=total_preco
                    )

                    for item_data in itens_data:
                        produto = Produto.objects.get(id=item_data["produto_id"])

                        if produto.quantidade < item_data["quantidade"]:
                            raise ValueError(f"Estoque insuficiente para o produto {produto.descricao}")

                        # Cria o ItemCompra para registrar o item na compra
                        ItemCompra.objects.create(
                            compra=compra,
                            produto=produto,
                            quantidade=item_data["quantidade"],
                            preco_unitario=produto.valor 
                        )

                        # Atualiza estoque e visibilidade
                        produto.quantidade -= item_data["quantidade"]
                        produto.exibir_no_carrinho = False 
                        produto.save()

                    return Response({"mensagem": "Compra finalizada com sucesso!"}, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({"erro": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
        else:
            return redirect('/login/')
        
    def get(self, request):
        if request.user.is_authenticated:
            compras = Compra.objects.all()
            serializer = CompraSerializer(compras, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return redirect('/login/')
    

def relatorio(request):
    if request.user.is_authenticated:
        total_itens_estoque = Produto.objects.aggregate(Sum('quantidade'))['quantidade__sum'] or 0
        valor_estoque = Produto.objects.aggregate(
            total=Sum(ExpressionWrapper(F('quantidade') * F('valor'), output_field=DecimalField()))
        )['total'] or 0.00
        total_itens_doados = ItemCompra.objects.aggregate(Sum('quantidade'))['quantidade__sum'] or 0
        valor_itens_doados = ItemCompra.objects.aggregate(
            total=Sum(ExpressionWrapper(F('quantidade') * F('preco_unitario'), output_field=DecimalField()))
        )['total'] or 0.00
        movimentacoes = Compra.objects.all().select_related('cliente')

        compras_detalhes = []
        for compra in movimentacoes:
            itens = ItemCompra.objects.filter(compra=compra).select_related('produto')
            compra_detalhes = {
                'id': compra.id,
                'cliente': f"{compra.cliente.first_name} {compra.cliente.last_name or ''}",
                'data': compra.data.strftime('%d/%m/%Y'),
                'gasto': f"R$ {compra.total_preco:.2f}",
                'status': 'Completado',
                'itens': [
                    {
                        'classificacao': item.produto.classe,
                        'tipo_embalagem': item.produto.tipo_produto,
                        'descricao': item.produto.descricao,
                        'quantidade': item.quantidade,
                        'preco': f"R$ {item.preco_unitario:.2f}"
                    } for item in itens
                ]
            }
            compras_detalhes.append(compra_detalhes)

        context = {
            'total_itens_estoque': total_itens_estoque,
            'valor_estoque': f'R$ {valor_estoque:.2f}',
            'total_itens_doados': total_itens_doados,
            'valor_itens_doados': f'R$ {valor_itens_doados:.2f}',
            'movimentacoes': movimentacoes,
            'compras_detalhes_json': json.dumps(compras_detalhes),  # Serializa para JSON
        }
        return render(request, 'relatorio.html', context)
    else:
        return redirect('/login/')