from django.shortcuts import render, redirect
from api.models import *
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

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
        return render(request, 'user/test2.html', {'usuario': user})
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

def cadastroCliente(request):
    usuarios = CustomUser.objects.filter(is_active=True)
    return  render(request, 'vendedor/cadastroCliente.html', {"usuarios": usuarios})
    
def estoque_adm(request):
    return render(request, 'admin/estoqueAdm.html')

def produto(request):
    produtos = Produto.objects.filter(is_disponivel=True)
    return render(request, 'vendedor/produto.html', {"produtos": produtos})

def cadastroVendedor(request):
    vendedores_list = CustomUser.objects.filter(tipo='vendedor')
    paginator = Paginator(vendedores_list, 5)  # 5 por página
    page_number = request.GET.get('page')
    vendedores = paginator.get_page(page_number)
    return  render(request, 'admin/cadastroVendedor.html', {"vendedores": vendedores})