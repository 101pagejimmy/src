# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

#BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#root of project

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'mf_$$e6u)vjs#j0zn9ifcx-anjtp#ey3xasz6fo2%))3nqy2ns'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'taylorhardie16@gmail.com'
EMAIL_HOST_PASSWORD = 'h@rd@s@motherfucker'
EMAIL_PORT = 587
EMAIL_USE_TLS = True


# Application definition

INSTALLED_APPS = (
    #django app
    'bootstrap_admin', 
    'django.contrib.admin',
    'registration',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #third party apps
    'crispy_forms',

    #review app
    'hvad',
    'review',
    'user_media',
    'generic_positions',


    #schedule Calander app
    "schedule",
    "djangobower",

    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",

    #tour app
    "tour",

    #pricing and booking tours
    "carts",
    "orders",

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)


RESERVATION_SPOTS_TOTAL= 100

ROOT_URLCONF = 'farmtofamily.urls'


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    'rest_framework.authentication.TokenAuthentication',
    ]
}


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,"templates"), os.path.join(BASE_DIR, 'tour', 'templates', 'tour'), os.path.join(BASE_DIR, 'review', 'templates', 'review'),],
        # 'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.request',
            ],
            'loaders': [
                ('pyjade.ext.django.Loader', (
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ))
            ],
        },
    },
]

WSGI_APPLICATION = 'farmtofamily.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
# Define the database manager to setup the various projects
# DATABASE_ROUTERS = ['manager.router.DatabaseAppsRouter']
# DATABASE_APPS_MAPPING = {'latlong_data': 't29_db'}




DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },

}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(os.path.join(os.path.dirname(BASE_DIR), "static_in_env", "static_root"))



STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'static', 'fonts' ),
    os.path.join(BASE_DIR, 'static', 'sass', 'bootstrap' ),
    os.path.join(BASE_DIR, 'static', 'sass', 'custom' ),
    os.path.join(BASE_DIR, 'static', 'sass', 'plugins', 'rd-navbar_includes' ),
                    )


BOWER_COMPONENTS_ROOT = os.path.join(BASE_DIR, 'components')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'djangobower.finders.BowerFinder',
)

BOWER_INSTALLED_APPS = (
    "jquery",
    "jquery-ui",
    "bootstrap",
    "fontawesome",
)



MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_in_env", "media_root")



#CRISPY FORM TAGS SETTINGS
CRISPY_TEMPLATE_PACK = 'bootstrap3'


#DJANGO REGISTRATION REDUX SETTINGS
ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_AUTO_LOGIN = True
SITE_ID = 1
LOGIN_REDIRECT_URL = '/'

GOOGLE_MAPS_API_KEY = "AIzaSyDyfNaXGaPZ_gq9eF1n38bEatS6R0aO_D4"
GEOPOSITION_GOOGLE_MAPS_API_KEY = "AIzaSyDyfNaXGaPZ_gq9eF1n38bEatS6R0aO_D4"



GEOS_LIBRARY_PATH = 'C:/Program Files/GDAL/geos_c.dll'


#BRAINTREE CONFIGURATION KEYS

BRAINTREE_PUBLIC = '3yywt6ngxhwf3zm4'
BRAINTREE_PRIVATE = '14cd6207a042e052c31b6d1fb7a5b88b'
BRAINTREE_MERCHANT_ID = '872z6b4yvvf6f734'
BRAINTREE_ENVIRONMENT = 'Sandbox'


