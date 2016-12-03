from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^signup/$',views.signup, name='signup'),
    url(r'^login/$', views.log_in, name='login'),
    url(r'^logout/$', views.log_out, name='logout'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^create-profile/$', views.create_profile, name='create_profile'),
    url(r'^favourite-list/$', views.favourite_list, name='favourite_list'),
]
