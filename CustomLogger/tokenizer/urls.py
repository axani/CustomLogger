from django.conf.urls import url
from django.conf import settings

from . import views

app_name = 'tokenizer'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create/$', views.create_token, name='create'),
    url(r'^%s/(?P<entered_token>.*)' % settings.TOKEN_SUBDOMAIN, views.token_page, name='token_page'),

]