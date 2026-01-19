from django.shortcuts import render, redirect
from api.models import *
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from collections import defaultdict
from django.contrib.auth import logout
import json




# View da página de login
def tela_login(request):
    return render(request, 'login.html')

def sair(request):
    logout(request)  # encerra a sessão do usuário
    return redirect('login')  # redireciona para a tela de login


@login_required(login_url='/login/')
def test1(request):
    user_id = request.user.id  

    user = CustomUser.objects.filter(id=user_id).first()
    if user:
        return render(request, 'user/test2.html', {'usuario': user})
    else:
        return redirect('login')


@login_required(login_url='/login/')
def SaldoUser(request):
    user_id = request.user.id  

    user = CustomUser.objects.filter(id=user_id).first()

    if user:
        compras = Compra.objects.filter(cliente=user).order_by('-data')
        return render(request, 'user/SaldoUser.html', {
            'usuario': user,
            'compras': compras
        })
    else:
        return redirect('login')  # Se o usuário não for encontrado, volta pro login


@login_required(login_url='/login/')
def test3(request):
    user_id = request.user.id  

    user = CustomUser.objects.filter(id=user_id).first()
    if user:
        return render(request, 'admin/estoqueAdm.html', {'usuario': user})
    else:
        return redirect('login')


@login_required(login_url='/login/')
def carrinho_vend(request):
    produtos =  Produto.objects.filter(exibir_no_carrinho=True)
    clientes = CustomUser.objects.filter(tipo='cliente', is_active=True)
    return render(request, 'vendedor/carrinho.html', {"produtos": produtos, "clientes": clientes})

# @login_required(login_url='/login/')
def cadastroUsuario(request): # so pra teste rapazeada
    usuarios = Produto.objects.filter(is_disponivel=True)
    
    # Filtrar apenas usuários ativos do tipo "cliente"
    # clientes_ativos = CustomUser.objects.filter(tipo='cliente', is_active=True)

    # # Filtrar apenas usuários ativos do tipo "vendedor"
    # vendedores_ativos = CustomUser.objects.filter(tipo='vendedor', is_active=True)

    # # Filtrar apenas usuários ativos do tipo "administrador"
    # administradores_ativos = CustomUser.objects.filter(tipo='administrador', is_active=True)
    return  render(request, 'componentes/TestpopUpUsuario.html', {"usuarios": usuarios})



def tela_inicial(request):
    return  render(request, 'index.html')


@login_required(login_url='/login/')
def relatorio(request):
     return render(request, 'admin/relatorio.html')


@login_required(login_url='/login/')
def cadastroCliente(request):
    user = request.user
    usuarios_list = CustomUser.objects.filter(tipo='cliente')
    paginator = Paginator(usuarios_list, 5)
    page_number = request.GET.get('page')
    usuarios = paginator.get_page(page_number)

    return render(request, 'vendedor/cadastroCliente.html', {
        "usuarios": usuarios,
        "user": user,
    })


@login_required(login_url='/login/')
def validarEmail(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        cliente_id = data.get('clienteId') or data.get('vendedorId')

        if not email:
            return JsonResponse({'error': 'Email não informado'}, status=400)

        query = CustomUser.objects.filter(email=email)
        if cliente_id:
            query = query.exclude(id=cliente_id)

        existe = query.exists()
        return JsonResponse({'existe': existe})
    
    return JsonResponse({'error': 'Método não permitido'}, status=405)

# @csrf_exempt
# # @login_required
# def toggle_cliente(request, cliente_id):
#     if request.method != "PATCH":
#         return HttpResponseNotAllowed(["PATCH"])

#     try:
#         data = json.loads(request.body)
#         is_active = data.get("is_active")
#         if type(is_active) is not bool:
#             return HttpResponseBadRequest("is_active deve ser true/false")

#         user = CustomUser.objects.get(id=cliente_id, tipo="cliente")
#         user.is_active = is_active
#         user.save()

#         return JsonResponse({"id": user.id, "is_active": user.is_active})

#     except CustomUser.DoesNotExist:
#         return JsonResponse({"error": "Cliente não encontrado."}, status=404)
#     except json.JSONDecodeError:
#         return JsonResponse({"error": "JSON inválido."}, status=400)
    

@login_required(login_url='/login/')    
def estoque_adm(request):
    produtos_list = Produto.objects.filter(ativo=True) # Todos os produtos ativos
    paginator = Paginator(produtos_list, 5)  # 5 produtos por página
    page_number = request.GET.get('page')  # Número da página na URL
    produtos = paginator.get_page(page_number)  # Página atual paginada

    context = {
        'produtos': produtos
    }
    return render(request, 'admin/estoqueAdm.html', context)


@login_required(login_url='/login/')
def produto(request):
    # Pega o filtro de classe da URL (se houver)
    classe_selecionada = request.GET.get('classe', None)
    
    # Filtra os produtos
    produtos = Produto.objects.filter(is_disponivel=True)
    
    if classe_selecionada and classe_selecionada != 'all':
        produtos = produtos.filter(classe=classe_selecionada)

    # Agrupar por classe
    produtos_por_classe = defaultdict(list)
    for produto in produtos:
        produtos_por_classe[produto.classe].append(produto)

    # Converter defaultdict para dict comum antes de passar para o template
    produtos_por_classe_dict = dict(produtos_por_classe)

    # Obter todas as classes disponíveis para o select
    todas_as_classes = Produto.objects.filter(is_disponivel=True).values_list('classe', flat=True).distinct()
    classes_disponiveis = [classe for classe in todas_as_classes if classe]  # Remove valores None

    return render(request, 'vendedor/produto.html', {
        "produtos_por_classe": produtos_por_classe_dict,
        "classes_disponiveis": classes_disponiveis,
        "classe_selecionada": classe_selecionada
    })


@login_required(login_url='/login/')
def cadastroVendedor(request):
    vendedores_list = CustomUser.objects.filter(tipo='vendedor')
    paginator = Paginator(vendedores_list, 5)  # 5 por página
    page_number = request.GET.get('page')
    vendedores = paginator.get_page(page_number)
    return  render(request, 'admin/cadastroVendedor.html', {"vendedores": vendedores})

