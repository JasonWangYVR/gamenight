from django.conf.urls import url

urlpatterns = [
    url(r'^signup/$', 'auth.views.signup', name='signup'),
    url(r'^login/$', 'auth.views.log_in', name='login'),
    url(r'^logout/$', 'auth.views.log_out', name='logout'),
    url(r'^profile/$', 'auth.views.profile', name='profile'),
]
