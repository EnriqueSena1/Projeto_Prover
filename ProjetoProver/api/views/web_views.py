from django.shortcuts import render, redirect
from api.models import *
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

# View da página de login
def tela_login(request):
    return render(request, 'index.html')

def test1(request):
    user_id = request.user.id  

    user = CustomUser.objects.filter(id=user_id).first()
    if user:
        return render(request, 'user/test2.html', {'usuario': user})
    else:
        return redirect('login')
    

def test2(request):
    user_id = request.user.id  

    user = CustomUser.objects.filter(id=user_id).first()
    if user:
        return render(request, 'user/test2.html', {'usuario': user})
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
     return render(request, 'vendedor/carrinho.html')

def cadastroUsuario(request):
    return  render(request, 'componentes/popUpUsuario.html')

    