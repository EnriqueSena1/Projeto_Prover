from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views.api_views import *
from .views.web_views import *

# ViewSets com Router
router = DefaultRouter()
router.register('usuarios', CustomUserViewSet)
router.register('produtos', ProdutoViewSet)
router.register('carrinhos', CarrinhoViewSet)
router.register('compras', CompraViewSet)
router.register('itensCompras', ItensCompraViewSet)


urlpatterns = [
    # Rotas automáticas dos ViewSets
    path('api/', include(router.urls)),

    # Rota para tela inicial de login
    path('', tela_inicial, name="inicio"),

    # APIView personalizada para usuários com lógica extra
    path('api/user/', User.as_view(), name='usuarios'),
    path('api/user/<int:id>/', User.as_view(), name='usuarioDetalhe'),

    # vai para o login
    path('', tela_login, name="inicio"),

    path('login/', tela_login, name="login"),
    path('api/login/', LoginView.as_view(), name='api_login'),

    path('HomeUser/', test2, name="home_user"),
    path('HomeAdm/', test1, name="home_adm"),
    path('HomeVend/', test3, name="home_vend"),
    path('CadastroUsuario/', cadastroUsuario, name="cadastro_user"),

    path('api/UsuarioLogado/', GetDadosUsuarioLogado.as_view(), name='dados_usuario_logado'),

    #Web e API Views ADMINISTRADOR
    path('estoqueadm/',estoque_adm, name="estoque_adm"),

    #Carrinho

    path('CarrinhoVend/',carrinho_vend, name="carrinho_vend"),
    path('CadastroCliente/', cadastroCliente, name="cadastro_cliente"),




]
