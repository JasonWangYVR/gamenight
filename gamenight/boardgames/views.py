from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.urls import reverse
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django import template
import string
from django.core.urlresolvers import resolve
from django.core.exceptions import ObjectDoesNotExist
from django.core import urlresolvers
from django.db.models import Q

from .models import BoardGame, Designer, Tag
from .forms import SearchForm, PerPageForm

# Create your views here.
def index(request):
	title = 'GameNight Board Game List'
	try:
		boardgame_list = BoardGame.objects.order_by('name')
	except ObjectDoesNotExist:
		HttpResponse('No boardgames available')
	# Pagination Start
	# Parsing pages and results for special conditions
	page = request.GET.get('page', 'a')
	page_size = request.GET.get('results', 'a')
	if page != 'a' and "results" in page:                #?page=int?results=int
		page_cutoff = page.find('?')
		page_size = page[page_cutoff : len(page)]
		page_cutoff2 = page_size.find('=')
		page_size = page_size[ page_cutoff2+1 : len(page_size)]
		page = page[0 : 0 + page_cutoff]
	elif page_size != 'a' and "page" in page_size:        #?results=int?page=int
		page_cutoff = page_size.find('?')
		page = page_size[page_cutoff : len(page_size)]
		page_cutoff2 = page.find('=')
		page = page[ page_cutoff2 + 1 : len(page)]
		page_size = page_size[0 : 0 + page_cutoff]
	elif ' ' in page:                                  #?page=page+per_page
		temp = page.split()
		page = temp[0]
		page_size = temp[1]
	elif ' ' in page_size:                                                  #?results=per_page+page
		page_size = request.GET.get('results', '20')
		current_page = 1
		if ' ' in page_size:
			temp = page_size.split()
			page_size = temp[0]
			current_page = temp[1]
			page = current_page
	else:
		page_size = 20
		page = page

	if int(page_size) == -1:
		page_size = boardgame_list.count()
	elif int(page_size) == 10 or 50 or 20:
		page_size = page_size
	else:
		page_size = 20

	paginator = Paginator(boardgame_list, page_size)
	try:
		boardgames = paginator.page(page)
	except PageNotAnInteger:
	# If page is not an integer, deliver first page.
		boardgames = paginator.page(1)
	except EmptyPage:
	# If page is out of range (e.g. 9999), deliver last page of results.
		boardgames = paginator.page(paginator.num_pages)
	#Pagination End

	context = {'boardgames': boardgames, 'title': title, 'search': SearchForm(), 'user': request.user}
	return render(request, 'boardgames/index.html', context)

# Not currently being used
# def next_detail(request, currBoardgameId, nextBoardgameId):
# 	return HttpResponse('Your in the view to get the next/prev detail page and redirect to it')

def detail(request, boardgameId):
	# will need favourite logic once user is added
	if request.GET.get('next'):
		# Quick way to go between detail pages. URL needs work
		next_boardgame = request.GET.get('next')
		boardgame = get_object_or_404(BoardGame, id=next_boardgame)
		prev_id = str(int(next_boardgame)-1)
		next_id = str(int(next_boardgame)+1)
		title = boardgame.name
		designers = boardgame.designed_by.all().values_list('name', flat=True)
		try:
			boardgame_next = BoardGame.objects.get(id=next_id)
		except BoardGame.DoesNotExist:
			next_id = None
		try:
			boardgame_prev = BoardGame.objects.get(id=prev_id)
		except BoardGame.DoesNotExist:
			prev_id = None
		context = {'boardgame': boardgame, 'title': title,
		'next_id': next_id, 'prev_id': prev_id, 'search': SearchForm(), 'designers': designers}
		return render(request, 'boardgames/detail.html/', context)
	else:
		boardgame = get_object_or_404(BoardGame, id=boardgameId)
		prev_id = str(int(boardgameId)-1)
		next_id = str(int(boardgameId)+1)
		title = boardgame.name
		designers = boardgame.designed_by.all().values_list('name', flat=True)
		try:
			boardgame_next = BoardGame.objects.get(id=next_id)
		except BoardGame.DoesNotExist:
			next_id = None
		try:
			boardgame_prev = BoardGame.objects.get(id=prev_id)
		except BoardGame.DoesNotExist:
			prev_id = None

		context = {'boardgame': boardgame, 'title': title,
		'next_id': next_id, 'prev_id': prev_id, 'search': SearchForm(), 'designers': designers}
		return render(request, 'boardgames/detail.html', context)


def search(request):
	title = 'Search Results'
	# Pagination Start
	if request.method == 'GET':
		page = request.GET.get('page', 'a')
		if page != 'a':
			page_cutoff = page.find('?')
			search = page[page_cutoff : len(page)]
			page_cutoff2 = search.find('=')
			search = search[ page_cutoff2+1 : len(search)]
			page = page[0 : 0 + page_cutoff]
			query_split = search.split(',')
			search_terms = search.split(',')
			for terms in query_split:
				search_terms.append(terms.replace(' ', ''))
			qobj = Q()
			for q in search_terms:
				qobj.add(Q(tag__tag_name__icontains=q), Q.OR)
				qobj.add(Q(name__icontains=q), Q.OR)
				# returns too many arbitrary results
				# qobj.add(Q(description__icontains=q), Q.OR)
			query2 = BoardGame.objects.filter(qobj).order_by('-bgg_bayesrating').distinct()
                
			paginator = Paginator(query2, 40)
			# page = request.GET.get('page')
			try:
				boardgames = paginator.page(page)
			except PageNotAnInteger:
			# If page is not an integer, deliver first page.
				boardgames = paginator.page(1)
			except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
				boardgames = paginator.page(paginator.num_pages)
			context = {'boardgames': boardgames, 'title': title, 'query': search, 'search': SearchForm(), 'user': request.user}
			return render(request, 'boardgames/search.html', context)

		else:
			search_form = SearchForm(request.GET)
			if search_form.is_valid():
				query = search_form.cleaned_data['q']
				query_split = query.split(',')
				search_terms = query.split(',')
				for terms in query_split:
					search_terms.append(terms.replace(' ', ''))
				qobj = Q()
				for q in search_terms:
					qobj.add(Q(tag__tag_name__icontains=q), Q.OR)
					qobj.add(Q(name__icontains=q), Q.OR)
					# returns too many arbitrary results
					# qobj.add(Q(description__icontains=q), Q.OR)
				query2 = BoardGame.objects.filter(qobj).order_by('-bgg_bayesrating').distinct()
	                
				paginator = Paginator(query2, 40)
				# page = request.GET.get('page')
				try:
					boardgames = paginator.page(page)
				except PageNotAnInteger:
				# If page is not an integer, deliver first page.
					boardgames = paginator.page(1)
				except EmptyPage:
				# If page is out of range (e.g. 9999), deliver last page of results.
					boardgames = paginator.page(paginator.num_pages)
				context = {'boardgames': boardgames, 'title': title, 'query': query, 'search': SearchForm(), 'user': request.user}
				return render(request, 'boardgames/search.html', context)

	context = {
		'search': SearchForm(),
	}
	return render(request, 'boardgames/search.html', context)


def add_favourite(request, boardgameId):
	boardgame = get_object_or_404(BoardGame, id=boardgameId)
	slug = boardgame.slug
	return HttpResponseRedirect(reverse('boardgames:detail', args=[boardgameId, slug]))
	# return HttpResponseRedirect(reverse('boardgames:detail', kwargs={'boardgameId': boardgameId}))


def remove_favourite(request, boardgameId):
	boardgame = get_object_or_404(BoardGame, id=boardgameId)
	slug = boardgame.slug
	return HttpResponseRedirect(reverse('boardgames:detail', args=[boardgameId, slug]))
	# return HttpResponseRedirect(reverse('boardgames:detail', kwargs={'boardgameId': boardgameId}))