from django.shortcuts import render, redirect
from api.models import *
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

# View da página de login
def tela_login(request):
    return render(request, 'index.html')