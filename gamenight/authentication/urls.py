from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^signup/$',views.signup, name='signup'),
    url(r'^login/$', views.log_in, name='login'),
    url(r'^logout/$', views.log_out, name='logout'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/edit-personal/$', views.edit_personal, name='edit_personal'),
    url(r'^profile/edit-profile/$', views.edit_profile, name='edit_profile'),
    url(r'^create-profile/$', views.create_profile, name='create_profile'),
    url(r'^favourite-list/$', views.favourite_list, name='favourite_list'),
    url(r'^(?P<boardgameId>[0-9]+)/remove_favourite/$', views.remove_favourite, name='remove_favourite'),

]
