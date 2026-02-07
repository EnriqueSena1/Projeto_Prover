from pathlib import Path
import os

# --- CAMINHOS BASE ---
BASE_DIR = Path(__file__).resolve().parent.parent

# --- SEGURANÇA ---
# Lê a chave do ambiente ou usa uma padrão se falhar (apenas para build)
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-chave-padrao-para-build')

# Debug deve ser False em produção. Se a variável não existir, assume False.
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Permite o domínio do Traefik ou qualquer um (*)
ALLOWED_HOSTS = ['*']

# --- APLICATIVOS INSTALADOS ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'api', # Seu app principal
]

# --- MIDDLEWARE (A Ordem aqui é CRUCIAL) ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    
    # [CORREÇÃO 1] O WhiteNoise deve vir LOGO APÓS o SecurityMiddleware
    "whitenoise.middleware.WhiteNoiseMiddleware",
    
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ProjetoProver.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ProjetoProver.wsgi.application'

# --- BANCO DE DADOS (Configuração para Docker) ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'bancoprover'),
        'USER': os.environ.get('DB_USER', 'root'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'db'), # No Docker, o host geralmente é o nome do serviço 'db'
        'PORT': '3306',
    }
}

# --- MODELO DE USUÁRIO ---
AUTH_USER_MODEL = 'api.CustomUser'

# --- VALIDADORES DE SENHA ---
AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

# --- INTERNACIONALIZAÇÃO ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --- ARQUIVOS ESTÁTICOS (CSS, JS, Imagens do Site) ---
STATIC_URL = '/static/'

# Onde o Django procura seus arquivos CSS personalizados (api/static/css/...)
# STATICFILES_DIRS = [ BASE_DIR / "api/static" ]
STATICFILES_DIRS = [
    BASE_DIR / "ProjetoProver" / "api" / "static",
]

# Onde o collectstatic vai juntar tudo (dentro do container)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# [CORREÇÃO 2] Configuração do WhiteNoise para servir os arquivos
# Usamos 'CompressedStaticFilesStorage' para evitar erros de manifesto com arquivos faltando
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

# --- ARQUIVOS DE MÍDIA (Uploads de Usuários) ---
MEDIA_URL = '/midia/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'midia')

# --- CONFIGURAÇÕES EXTRAS ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 5,
}

LOGIN_URL = '/login/'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# --- [CORREÇÃO 3] LOGS DETALHADOS PARA DEBUG ---
# Isso fará os erros aparecerem no comando 'docker service logs'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG', # Mostra detalhes de erros 404 e 500
            'propagate': True,
        },
        'whitenoise': {
            'handlers': ['console'],
            'level': 'DEBUG', # Mostra por que um arquivo estático não carregou
        },
    },
}