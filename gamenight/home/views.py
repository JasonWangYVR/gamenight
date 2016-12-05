from django.shortcuts import get_object_or_404, render, redirect
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from boardgames.forms import SearchForm
from django.contrib.auth.models import User
from authentication.models import UserProfile
from events.models import Event
from events.forms import SearchEventsForm

def index(request):

	if request.user.is_authenticated():
		try:
			user = UserProfile.objects.get(user=request.user)
			attending = user.attending_events.all()
			event = attending.order_by('event_date')[:5]

			#TODO: filter for public
			event_list = Event.objects.filter(private_event=False)
			# event_list = Event.objects.all()
			page = request.GET.get('page')
			paginator = Paginator(event_list, 10)
			try:
				events = paginator.page(page)
			except PageNotAnInteger:
			# If page is not an integer, deliver first page.
				events = paginator.page(1)
			except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
				events = paginator.page(paginator.num_pages)

			context = {
				'user':request.user,
				'events':events,
				'events_u':event,
				'search':SearchForm(),
				'search_p': SearchEventsForm()
			}
			return render(request, 'home/index.html', context)
		except ObjectDoesNotExist:
			return redirect('authentication:create_profile')
	else:
		event_list = Event.objects.filter(private_event=False)
		# event_list = Event.objects.all()
		page = request.GET.get('page')
		paginator = Paginator(event_list, 10)
		try:
			events = paginator.page(page)
		except PageNotAnInteger:
		# If page is not an integer, deliver first page.
			events = paginator.page(1)
		except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
			events = paginator.page(paginator.num_pages)

		context = {
			'user':request.user,
			'events':events,
			'search':SearchForm(),
			'search_p': SearchEventsForm()
		}
		return render(request, 'home/index.html', context)
