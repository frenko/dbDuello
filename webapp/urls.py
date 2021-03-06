from django.conf.urls import url

from . import views

app_name = 'webapp'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^latest/$', views.latest, name='latest'),
    url(r'^add/$', views.add, name='add'),
    url(r'^allopera/$', views.allopera, name='allopera'),
    url(r'^view/(?P<opera_id>[0-9]+)/$', views.view_opera, name='view_opera'),
    url(r'^mod/(?P<opera_id>[0-9]+)/$', views.mod_opera, name='mod_opera'),
    url(r'^delete/(?P<opera_id>[0-9]+)/$', views.delete, name='delete'),
    url(r'^userprofile/$', views.user_profile, name='user_profile'),
]
