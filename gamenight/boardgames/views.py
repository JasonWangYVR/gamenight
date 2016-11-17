from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django import template
import string
from django.core.urlresolvers import resolve

from .models import BoardGame, Designer, Tag
from .forms import SearchForm, PerPageForm

# Create your views here.
def index(request):
	title = 'GameNight Board Game List'
	boardgame_list = BoardGame.objects.order_by('name')
	# Pagination Start
	# Parsing pages and results for special conditions
	page = request.GET.get('page', 'a')        
	page_size = request.GET.get('results', 'a')
	if page != 'a' and "results" in page:                #?pags=int?results=int
		page_cutoff = page.find('?')
		page_size = page[page_cutoff : len(page)]
		page_cutoff2 = page_size.find('=')
		page_size = page_size[ page_cutoff2+1 : len(page_size)]
		page = page[0 : 0 + page_cutoff]
	elif page_size != 'a' and "page" in page_size:        #?results=int?page=int
		print(page_size)
		page_cutoff = page_size.find('?')
		page = page_size[page_cutoff : len(page_size)]
		print(page)
		page_cutoff2 = page.find('=')
		page = page[ page_cutoff2 + 1 : len(page)]
		page_size = page_size[0 : 0 + page_cutoff]
	elif ' ' in page:                                  #?page=page+per_page
		print('in pages')
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

	# if request.method == 'GET':
	# 	print('in get')
	# 	s_form = SearchForm(request.GET)
	# 	p_form = PerPageForm(request.GET)
	# 	# check whether it's valid:
	# 	if s_form.is_valid():
	# 		s_form.process()
	# 		page = s_form.cleaned_data['want_page']
	# 		url = '/boardgames/?page='+str(page)
	# 		return HttpResponseRedirect(url)
	# 	elif p_form.is_valid():
	# 		p_form.process()
	# 		per_page = p_form.cleaned_data['page_size']
	# 		print(current_page)
	# 		if int(per_page) == -1:
	# 			per_page = boardgame_list.count()
	# 		url = '/boardgames/?pages='+str(current_page)+'?results='+str(per_page)
	# 		return HttpResponseRedirect(url)

	context = {'boardgames': boardgames, 'title': title}
	return render(request, 'boardgames/index.html', context)

def detail(request, id):
    boardgame = get_object_or_404(BoardGame, id=id)
    obj = BoardGame.objects.get(id=id)
    title = obj.name
    return render(request, 'boardgames/detail.html', {'boardgame': boardgame, 'title': title})
