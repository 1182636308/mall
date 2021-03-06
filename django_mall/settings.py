"""
Django settings for django_mall project.

Generated by 'django-admin startproject' using Django 1.11.29.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'w*%9-!72yzj$e^#4*$g=yj6va1mx(2r&knqj6)m4^^g*uj%z)t'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 富文本编辑器的配置
    'ckeditor',
    # 'ckeditor_uploader'
    # xadmin 的配置
    'xadmin',
    'crispy_forms',
    'reversion',
    'mall.apps.MallConfig',  # 商品模块
    'accounts.apps.AccountsConfig', # 用户账户模块
    'mine.apps.MineConfig',  # 个人中心模块
    'system.apps.SystemConfig', # 系统模块
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 自定义的中间件
    # 'utils.middleware.ip_middleware',
    # 'utils.middleware.MallAuthMiddleware',
]

ROOT_URLCONF = 'django_mall.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 自己添加的渲染上下文
                'system.context_processors.const',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_mall.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_mall',
        'USER': 'root',
        'PASSWORD': '9079617114',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]


# 使用自定义的用户模型
AUTH_USER_MODEL = 'accounts.User'

# 如果用户没有登录进入了需要登录的页面，则跳转到登录页面
LOGIN_URL = '/accounts/user/login/'



# 自己上传的图片地址配置
MEDIA_ROOT = os.path.join(BASE_DIR, 'medias')
MEDIA_URL = '/medias/'


# 富文本编辑器中的上传地址配置
CKEDITOR_UPLOAD_PATH = os.path.join(MEDIA_ROOT, 'uploads/')

# CSRF的设置
CSRF_USE_SESSIONS = False


# 邮箱发送的配置
# EMAIL_HOST = 'smtp.qq.com'
# EMAIL_HOST_USER = '1182636308@qq.com'
# EMAIL_HOST_PASSWORD = 'zqvaepjozciehfff'
# 将异常发给管理员
# SERVER_EMAIL = '1182636308@qq.com'
# ADMINS = [('admin','1182636308@qq.com')]

# 日志的配置
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'log_file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': os.path.join(BASE_DIR,'log/debug.log')
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['log_file'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     },
# }