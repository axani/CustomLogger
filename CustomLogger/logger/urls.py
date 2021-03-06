from django.conf.urls import url
from django.conf import settings

from . import views

app_name = 'logger'
urlpatterns = [
    url(r'^home/(?P<token>.*)$', views.home, name='home'),
    url(r'^add/(?P<target_type>.*)$', views.add, name='add'),
    # url(r'^log/$', views.log, name='log'),
    url(r'^update/(?P<action>.*)/(?P<target_type>.*)/(?P<target_id>.*)$', views.update, name='update'),
]