from django.conf.urls import url

from . import views

app_name = 'events'
urlpatterns = [
    #handles requests for index
    url(r'^$', views.IndexView.as_view(), name='index'),
    #handles requests for specific event according to event_id
    url(r'^(?P<event_id>[0-9]+)/$', views.detail, name='detail'),
    ]
