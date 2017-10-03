from django.conf.urls import url
from django.conf import settings

from . import views

urlpatterns = [
    url(r'^%s/(?P<entered_token>.*)' % settings.TOKEN_SUBDOMAIN, views.token_page, name='token_page'),
 #   url(r'^$', views.index, name='index'),

]