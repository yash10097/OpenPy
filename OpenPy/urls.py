"""      Please refer to the license file for complete details. 
  *      Project: OpenPy
  *      Developer: Yash Lamba
  *      Institute: Indraprastha Institute of Information Technology, Delhi
  *      Advisor: Pandarasamy Arjunan, Dr. Pushpendra Singh
"""

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from views import init
from functions import LoadConfig
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', TemplateView.as_view(template_name='base.html')),
	url(r'^confirm(?P<pending_apikey>.+)$', 'views.confirm',name='pending_apikey'),
	url(r'^signup/$', 'views.signup'),
	url(r'^explorer/$', 'views.explorer'),
	url(r'^captcha/', include('captcha.urls')),
	url(r'^documentation/$', 'views.documentation'),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^python/(?P<url>.+)/$','views.main',name='url'),
)

init()
LoadConfig()
