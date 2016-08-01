from django.conf.urls import url

from . import views

app_name = 'webapp'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    # ex: /webapp/5/
    url(r'^(?P<opera_id>[0-9]+)/$', views.view_opera, name='view_opera'),
]
