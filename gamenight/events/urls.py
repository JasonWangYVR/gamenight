from django.conf.urls import url

from . import views

app_name = 'events'
urlpatterns = [
    #handles requests for index
    url(r'^$', views.index, name='index'),
    #handles requests for specific event according to event_id
    url(r'^(?P<event_id>[0-9]+)/$', views.detail, name='detail'),
	#event creation
	url(r'^create/$', views.create_event, name='create',),
    #question creation
	url(r'^createquestion/(?P<event_id>[0-9]+)/$', views.create_question, name='createquestion',),
    #edits event
	url(r'^editevent/(?P<pk>\d+)/$', views.EditEventView.as_view(),
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
