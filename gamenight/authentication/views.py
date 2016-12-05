from django.shortcuts import render, redirect
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from authentication.forms import *
from boardgames.forms import SearchForm
from authentication.models import UserProfile

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
                return render(request, 'authentication/signup.html', {'registered': registered,})
        else:
            form = UserForm()

        # template = loader.get_template('authentication/signup.html')
        # context = RequestContext(request, {
        #     'form': form,
        #     'registered': registered,
        # })
        #return HttpResponse(template.render(context))
        return render(request, 'authentication/signup.html', {'form': form, 'registered': registered})
    else:
        return redirect('home:index')

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

        # template = loader.get_template('authentication/login.html')
        # context = RequestContext(request, {
        #     'form': log_form,
        #     'wrong': wrong,
        # })
        #return HttpResponse(template.render(context))
        return render(request, 'authentication/login.html', {'form':log_form, 'wrong':wrong,})
    else:
        try:
            profile = UserProfile.objects.filter(user=request.user, deleted=False)
            return redirect('home:index')
        except ObjectDoesNotExist:
            context = {'user':request.user}
            return render(request, 'authentication/profile.html', context)

def log_out(request):
    logout(request)
    #return redirect('home:index')
    return redirect('authentication:login')


def profile(request):
    #return render(request, 'authentication/profile.html', {'search': SearchForm()}) ???
    if request.user.is_authenticated():
        try:
            profile = UserProfile.objects.get(user=request.user, deleted=False)
            context = {
                'user':request.user,
                'profile':profile,
                'search_form':SearchForm(),
            }
            return render(request, 'authentication/profile.html', context)
        except ObjectDoesNotExist:
            return redirect('authentication:create_profile')
    else:
        return redirect('authentication:login')

def create_profile(request):
    if request.user.is_authenticated():
        profile_created = False
        try:
            profile = UserProfile.objects.get(user=request.user, deleted=False)
            #context = {
            #    'user':request.user,
            #    'profile':profile, #was previously profile but his doesn't work with the way the template was described
            #}
            return render(request, 'authentication/profile.html', {'user':request.user,'profile':True})
        except ObjectDoesNotExist:
            if request.method == 'POST':
                form = ProfileForm(request.POST)
                if form.is_valid():
                    profile = form.save(commit=False)
                    profile.user = request.user
                    profile.deleted = False
                    profile.save()
                    profile_created = True
                context = {
                    'profile_created':profile_created
                }
                #template = loader.get_template('authentication/create_profile.html')
                #context = RequestContext(request, {
                #    'form': form,
                #    'profile_created': profile_created,
                #})
                return render(request, 'authentication/create_profile.html', {'profile_created':profile_created})
            else:
                form=ProfileForm()
            return render(request, 'authentication/create_profile.html', {'form':form, 'profile_created':profile_created})
    else:
        return redirect('authentication:login')

#TODO
def edit_profile(request):
    if request.user.is_authenticated():
        try:
            profile = UserProfile.objects.get(user=request.user, deleted=False)
        except ObjectDoesNotExist:
            return redirect('authentication:profile')

        if request.method == "POST":
            form = EditProfileForm(request.POST, instance=profile)
            if form.is_valid():
                profile.save()
            return redirect('authentication:profile')
        else:
            form = EditProfileForm(instance=profile)
        return render(request, 'authentication/edit_profile.html', {'form': form})
    else:
        return redirect('authentication:login')

def edit_personal(request):
    if request.user.is_authenticated():
        user = request.user
        if request.method == "POST":
            form = EditUserForm(request.POST, instance=user)
            if form.is_valid():
                user.save()
            return redirect('authentication:profile')
        else:
            form = EditUserForm(instance=user)
        return render(request, 'authentication/edit_personal.html', {'form': form})
    else:
        return redirect('authentication:login')

def favourite_list(request):
    # if request.user.is_authenticated():
    context = {'search': SearchForm()}
    return render(request, 'authentication/favourite_list.html', context)