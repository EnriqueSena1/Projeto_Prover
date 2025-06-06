from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views.api_views import *
from .views.web_views import *

# ViewSets com Router
router = DefaultRouter()
router.register('usuarios', CustomUserViewSet)
router.register('clientes', ClienteViewSet)
router.register('produtos', ProdutoViewSet)
router.register('carrinhos', CarrinhoViewSet)
router.register('compras', CompraViewSet)
router.register('itens-compras', ItensCompraViewSet)


urlpatterns = [
    # Rotas automáticas dos ViewSets
    path('api/', include(router.urls)),

    # APIView personalizada para usuários com lógica extra
    path('api/user/', User.as_view(), name='usuarios'),
    path('api/user/<int:id>/', User.as_view(), name='usuarioDetalhe'),

    # vai para o login
    path('', tela_login, name="login"),
]

