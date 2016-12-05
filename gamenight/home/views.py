from django.shortcuts import get_object_or_404, render, redirect
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from boardgames.forms import SearchForm
from django.contrib.auth.models import User
from authentication.models import UserProfile
from events.models import Event

def index(request):
	if request.user.is_authenticated():
		user = UserProfile.objects.get(user=request.user)
		attending = user.attending_events.all()
		event = attending.order_by('event_date')[:5]
		context = {
			'user':request.user,
			'events':event,
			'search':SearchForm(),
		}
		return render(request, 'home/index.html', context)
	else:
		context = {
			'user':request.user,
			'search':SearchForm(),
		}
		return render(request, 'home/index.html', context)