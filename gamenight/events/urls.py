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
    #choice creation
	url(r'^createchoice/(?P<question_id>[0-9]+)/$', views.create_choice, name='createchoice',),
	#message creation
	url(r'^createmessage/(?P<event_id>[0-9]+)/$', views.create_message, name='createmessage',),
    #edits event
	url(r'^editevent/(?P<event_id>\d+)/edit/$', views.edit_event, name='editevent',),
    #edit question
    url(r'^editq/(?P<question_id>\d+)/$', views.edit_question, name='editquestion',),
    #edit message
    url(r'^editm/(?P<message_id>\d+)/$', views.edit_message, name='editmessage',),
    #delete question
    url(r'^deleteq/(?P<question_id>\d+)/$', views.delete_question, name='deletequestion',),
    #edit choice
    url(r'^editc/(?P<choice_id>\d+)/$', views.edit_choice, name='editchoice',),
    #delete choice
    url(r'^deletec/(?P<choice_id>\d+)/$', views.delete_choice, name='deletechoice',),
	#delete message
    url(r'^deletem/(?P<message_id>\d+)/$', views.delete_message, name='deletemessage',),
	#delete event
    url(r'^deleteevent/(?P<event_id>\d+)/$', views.delete_event, name='delete_event',),
	#vote
    url(r'^(?P<choice_id>[0-9]+)/vote/$', views.vote, name='vote'),

    url(r'^public-events/$', views.public_events, name='public_events',),
	
	url(r'^searchevent/$', views.search_event, name='search_event')

    #creates choice
    #url(r'^addq/(?P<pk>\d+)/$', views.CreateChoiceView.as_view(), name='addchoice',),
    #VOID creates question
    #url(r'^addq/(?P<pk>\d+)/$', views.CreateQuestionView.as_view(), name='addquestion',),
    ]
