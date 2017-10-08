from django.conf.urls import url
from django.conf import settings

from . import views

app_name = 'logger'
urlpatterns = [
    url(r'^home/(?P<token>.*)$', views.home, name='home'),
    url(r'^add/$', views.add_log_button, name='add_log_button'),
    url(r'^log/$', views.log, name='log'),
    url(r'^update_log/undo/(?P<undo_action>.*)/(?P<log_id>.*)$', views.undo_update_log, name='undo_update_log'),
    url(r'^update_log/(?P<action>.*)$', views.update_log, name='update_log'),

]