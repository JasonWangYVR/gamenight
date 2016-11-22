from django.shortcuts import render, redirect
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import Http404, HttpResponse, HttpResponseRedirect
from authentication.forms import *
from authentication.models import GNUser

def signup(request):
    if not request.user.is_authenticated():
        registered = False
        if request.POST:
            form = UserForm(request.POST)
            if form.is_valid():
                if form.cleaned_data['password'] and form.cleaned_data['passwordretry']:
                    user = User.objects.create_user(
                        username=form.cleaned_data['username'],
                        first_name=form.cleaned_data['first_name'],
                        last_name=form.cleaned_data['last_name'],
                        password=form.cleaned_data['password'],
                        email=form.cleaned_data['email']
                    )
                registered = True
                template = loader.get_template('authentication/signup.html')
                context = RequestContext(request, {'registered':registered })
                #return HttpResponse(template.render(context))
                return render(request, 'authentication/signup.html', {'registered': registered,})
        else:
            form = UserForm()

        template = loader.get_template('authentication/signup.html')
        context = RequestContext(request, {
            'form': form,
            'registered': registered,
        })
        #return HttpResponse(template.render(context))
        return render(request, 'authentication/signup.html', {'form':form, 'registered':registered,})
    else:
        return redirect('authentication:login')

def log_in(request):
    if not request.user.is_authenticated():
        wrong = False
        if request.method == 'POST':
            log_form = LoginForm(request.POST)
            if log_form.is_valid():
                usern = log_form.cleaned_data['username']
                passw = log_form.cleaned_data['password']
                user = authenticate(username=usern, password=passw)
                if user:
                    if user.is_active:
                        login(request, user)
                        return redirect('authentication:profile')
                else:
                    wrong = True
        else:
            log_form = LoginForm()

        template = loader.get_template('authentication/login.html')
        context = RequestContext(request, {
            'form': log_form,
            'wrong': wrong,
        })
        #return HttpResponse(template.render(context))
        return render(request, 'authentication/login.html', {'form':log_form, 'wrong':wrong,})
    else:
        return redirect('authentication:profile')

def log_out(request):
    logout(request)
    #return redirect('home:index')
    return redirect('authentication:login')

def profile(request):
    return render(request, 'authentication/profile.html')
