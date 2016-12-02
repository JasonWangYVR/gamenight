from django.conf.urls import url

from . import views

app_name = 'events'
urlpatterns = [
    #handles requests for index
    url(r'^$', views.IndexView.as_view(), name='index'),
    #handles requests for specific event according to event_id
    url(r'^(?P<event_id>[0-9]+)/$', views.detail, name='detail'),
	#event creation
	url(r'^new$', views.CreateEventView.as_view(),
    name='create',),
    #edits event
	url(r'^edit/(?P<pk>\d+)/$', views.EditEventView.as_view(),
    name='editevent',),
    #creates question
	url(r'^addq/(?P<pk>\d+)/$', views.CreateQuestionView.as_view(),
    name='addquestion',),
    #edit question
    url(r'^editq/(?P<pk>\d+)/$', views.EditQuestionView.as_view(),
    name='editquestion',),
    #creates choice
    url(r'^addq/(?P<pk>\d+)/$', views.CreateChoiceView.as_view(),
    name='addchoice',),
    ]
