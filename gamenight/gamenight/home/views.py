from django.shortcuts import render
from boardgames.forms import SearchForm

def index(request):
        return render(request, 'home/index.html', {'search': SearchForm()})
