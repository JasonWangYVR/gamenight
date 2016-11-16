from django.conf.urls import url

from . import views

app_name = 'boardgames'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^[?]pages=([0-9]+)/([?]results=([0-9]+))?/$', views.index, name='index'),
    # ex: /boardgames/5/
    url(r'^(?P<id>[0-9]+)(?:/([\w-]+))?/$', views.detail, name='detail'),
    # The next two urls are in case multiple urls to the same destination is better than an optional path
    #url(r'^(?P<id>[0-9]+)/$', views.detail, name='detail'),
    #url(r'^(?P<id>[0-9]+)?/([\w-]+)/$', views.detail, name='detail'),

    # ex: /boardgames/monopoly-go/
#    url(r'^(?P<pk>[0-9]+)/$', views.detail, name='detail'),
]