from django.shortcuts import render, redirect
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login, logout
from django.http import Http404, HttpResponse, HttpResponseRedirect
from auth.forms import *
from auth.models import GNUser

def signup(request):
    if not request.user.is_authenticated():
        registered = False
        if request.method == 'POST':
            form = UserForm(request.POST)
            if form.is_valid():
                if form.cleaned_data['password'] and
                form.cleaned_data['passwordretry']:
                    user = GNUser.objects.create_user(
                        username=form.cleaned_data['username'],
                        first_name=form.cleaned_data['first_name'],
                        last_name=form.cleaned_data['last_name'],
                        password=form.cleaned_data['password'],
                        email=form.cleaned_data['email']
                    )
                registered = True
                template = loader.get_template('auth/signup.html')
                context = RequestContext(request, {'registered':registered })
                return HttpResponse(template.render(context))
        else:
            form = UserForm()

        template = loader.get_template('auth/signup.html')
        context = RequestContext(request, {
            'form': form,
            'registered': registered,
        })
        return HttpResponse(template.render(context))

    else:
        return redirect('auth:login')

def log_in(request):
    if not request.user.is_authenticated():
        wrong = False
        if request.method == 'POST':
            log_form = LoginForm(request.POST)
            if form.is_valid():
                usern = log_form.cleaned_data['username']
                passw = log_form.cleaned_data['password']
                user = authenticate(username=usern, password=passw)
                if user:
                    if user.is_active:
                        login(request, user)
                        return redirect('home:index')
                else:
                    wrong = True
        else:
            log_form = LoginForm()

        template = loader.get_template('auth/login.html')
        context = RequestContext(request, {
            'form': log_form,
            'wrong': wrong,
        })
        return HttpResponse(template.render(context))
    else:
        return redirect('home:index')

def log_out(request):
    logout(request)
    return redirect('home:index')
