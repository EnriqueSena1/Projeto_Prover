from django.shortcuts import render, redirect
from api.models import *
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

# View da página de login
def tela_login(request):
    return render(request, 'login.html')

def test1(request):
    user_id = request.user.id  

    user = CustomUser.objects.filter(id=user_id).first()
    if user:
        return render(request, 'user/test2.html', {'usuario': user})
    else:
        return redirect('login')
    

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
    

def test3(request):
    user_id = request.user.id  

    user = CustomUser.objects.filter(id=user_id).first()
    if user:
        return render(request, 'admin/estoqueAdm.html', {'usuario': user})
    else:
        return redirect('login')

def carrinho_vend(request):
    produtos =  Produto.objects.filter(exibir_no_carrinho=True)
    clientes = CustomUser.objects.filter(tipo='cliente', is_active=True)
    return render(request, 'vendedor/carrinho.html', {"produtos": produtos, "clientes": clientes})

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

def relatorio(request):
     return render(request, 'admin/relatorio.html')

def cadastroCliente(request):
    user = request.user  # Usuário logado
    usuarios = CustomUser.objects.filter(tipo='cliente')  # Lista de clientes
    return render(request, 'vendedor/cadastroCliente.html', {
        "usuarios": usuarios,
        "user": user, 
    })

def validarEmail(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        cliente_id = data.get('clienteId') 

        if not email:
            return JsonResponse({'error': 'Email não informado'}, status=400)

        query = CustomUser.objects.filter(email=email, tipo="cliente")
        if cliente_id:
            query = query.exclude(id=cliente_id)

        existe = query.exists()
        return JsonResponse({'existe': existe})
    
    return JsonResponse({'error': 'Método não permitido'}, status=405)

@csrf_exempt
# @login_required
def toggle_cliente(request, cliente_id):
    if request.method != "PATCH":
        return HttpResponseNotAllowed(["PATCH"])

    try:
        data = json.loads(request.body)
        is_active = data.get("is_active")
        if type(is_active) is not bool:
            return HttpResponseBadRequest("is_active deve ser true/false")

        user = CustomUser.objects.get(id=cliente_id, tipo="cliente")
        user.is_active = is_active
        user.save()

        return JsonResponse({"id": user.id, "is_active": user.is_active})

    except CustomUser.DoesNotExist:
        return JsonResponse({"error": "Cliente não encontrado."}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido."}, status=400)
    
def estoque_adm(request):
    produtos = Produto.objects.filter(is_disponivel=True)
    context = {
        'produtos': produtos
    }
    return render(request, 'admin/estoqueAdm.html', context)

def produto(request):
    produtos = Produto.objects.filter(is_disponivel=True)
    return render(request, 'vendedor/produto.html', {"produtos": produtos})

def cadastroVendedor(request):
    vendedores_list = CustomUser.objects.filter(tipo='vendedor')
    paginator = Paginator(vendedores_list, 5)  # 5 por página
    page_number = request.GET.get('page')
    vendedores = paginator.get_page(page_number)
    return  render(request, 'admin/cadastroVendedor.html', {"vendedores": vendedores})

