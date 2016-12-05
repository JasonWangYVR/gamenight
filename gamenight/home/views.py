from django.shortcuts import get_object_or_404, render, redirect
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from boardgames.forms import SearchForm
from django.contrib.auth.models import User
from authentication.models import UserProfile
from events.models import Event

def index(request):
    event=Event.objects.order_by('event_date')[:5]
        #return render(request, 'home/index.html', {'search': SearchForm(), 'user':request.user}) #HEAD

 #   if request.user.is_authenticated():
 #       try:
  #          context = {
 #               'user':request.user,
 #           }
 #           return render(request, 'home/index.html', context)
 #       except ObjectDoesNotExist:
 #           return redirect('authentication:sign_up')
 #   else:
 #       return render(request, 'home/index.html', {'search': SearchForm()})
    context = {
        'user':request.user,
		'events':event,
    }
    return render(request, 'home/index.html', context)
