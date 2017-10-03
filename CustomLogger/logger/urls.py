from django.conf.urls import url
from django.conf import settings

from . import views

app_name = 'logger'
urlpatterns = [
    url(r'^add/$', views.add_log_button, name='add_log_button'),
    url(r'^log/$', views.log, name='log'),

]