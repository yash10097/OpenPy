"""      Please refer to the license file for complete details. 
  *      Project: OpenPy
  *      Developer: Yash Lamba
  *      Institute: Indraprastha Institute of Information Technology, Delhi
  *      Advisor: Pandarasamy Arjunan, Dr. Pushpendra Singh
"""

"""
Django settings for OpenPy project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.normpath(os.path.dirname(__file__)+'/..')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '46rrf8lp^&2t1hg5k-4r)91kp!3^oyedtym_74^o3_el^4o0af'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True
INTERNAL_IPS = ('127.0.0.1',)

ALLOWED_HOSTS = []

ADMINS = (
)
# Application definition

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'south',
    'captcha',
    'registration',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
)

ROOT_URLCONF = 'OpenPy.urls'

WSGI_APPLICATION = 'OpenPy.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
)


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

#CACHE
LOCATION='127.0.0.1:11211'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': LOCATION,
    }
}



# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/m/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/s/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'bootstrap'),
    os.path.join(BASE_DIR, 'assets'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


#Defining Other Constants
HOST_IP='127.0.0.1' 
PORT_NUMBER='8000'

#Email Variables
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

#URL Paths
PACKAGE_PATH="s_package"
TEMP_OBJECTS_LOCATION="tmp"
PROFILE_INFO="profile"
SIGNUP_CONFIRM="confirm"
USER_PACKAGE="user_packages"
UNRESTRICTED_ACCESS="package"
SHARED_TEMP_OBJECTS_LOCATION='shared_tmp'
UPLOAD="upload"
SHARED_FOLDER="shared"

#Registration EMAILS
ACCOUNT_CONFIRMATION='Dear User,\nClick to confirm your account %s'
ACCOUNT_CONFIRMATION_SUBJECT='OpenPy Account Confirmation'
APIKEY_RECOVERY_EMAIL='Dear User,\nYour apikey is %s.\nIn case you have not requested the key then please ignore the email.'
APIKEY_RECOVERY_EMAIL_SUBJECT='OpenPy APIKEY Recovery'
APIKEY_DELIVERY_EMAIL='Dear User,\nYour apikey is %s. Please include this apikey in the header of your request with the field name \'APIKEY\''
APIKEY_DELIVERY_EMAIL_SUBJECT='Your OpenPy APIKEY'

#Registration Page Messages
PENDING_CONFIRMATION="You already have a pending confirmation email."
ALREADY_REGISTERED="You are already a registered user."
THANKS_MESSAGE="Thank You for Registering. Please check your inbox and confirm the registration within the next 24 hours."
APIKEY_EMAIL_DELIVERY_CONFIRMATION="Your APIKEY has been sent to your inbox."
INCORRECT_RECOVERY_REQUEST="Playing smart eh! Please register first, then misplace your apikey to recover it."
APIKEY_DELIVERY="Your APIKEY has been sent to your inbox. Thank You for registering with OpenPy."
LINK_EXPIRY="The link has expired"

#Error Messages
INVALID_USER="Invalid User"
INVALID_PACKAGE="Invalid Package Name"
INVALID_METHOD="Invalid Method Name"
INVALID_OUTPUT_FORMAT="Invalid Output Format"
INAPPROPRIATE_ARGUMENTS="Missing arguments"
INVALID_REQUEST="Invalid Request"
INVALID_OBJECT="Invalid Object Requested"
BUILTIN_METHOD="No documentation for builtin method"
SUCCESS="Success"
FILE_NOT_FOUND="File Not Found"
APIKEY_FIELD_MISSING="No apikey in request"
INVALID_FILE_TYPE="Only python files are supported"
INVALID_FILE_NAME="Invalid File Name"
REGISTRATION_FAILURE_MESSAGE="Registration has been disabled due to technical issues"
LIMIT_REQUEST=100

#Header Fields
APIKEY='HTTP_APIKEY'

#APIKEY Related Files
REGISTERED_APIKEYS='apikeys.json'
UNCONFIRMED_USERKEYS='pending.json'
PROFILE24='profile24.json'
PROFILE='profile.json'

#Signup Page Button Names
SIGNUP_BUTTON='signup'
RECOVERY_BUTTON='recover'

#OUTPUT formats with the default being json
OUTPUT_FORMATS=['json','ascii','save']
