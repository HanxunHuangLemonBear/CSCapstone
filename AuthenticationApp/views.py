"""AuthenticationApp Views

Created by Naman Patwari on 10/4/2016.
"""

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages


from .forms import LoginForm, RegisterForm, UpdateForm, UpdateProfessorForm,UpdateEngineersForm,UpdateStudentForm
from .models import MyUser
import logging

# Auth Views
target_user = None

def auth_login(request):
	form = LoginForm(request.POST or None)
	next_url = request.GET.get('next')
	if next_url is None:
		next_url = "/"
	if form.is_valid():
		email = form.cleaned_data['email']
		password = form.cleaned_data['password']
		user = authenticate(email=email, password=password)
		if user is not None:
			messages.success(request, 'Success! Welcome, '+(user.first_name or ""))
			login(request, user)
			return HttpResponseRedirect(next_url)
		else:
			messages.warning(request, 'Invalid username or password.')

	context = {
		"form": form,
		"page_name" : "Login",
		"button_value" : "Login",
		"links" : ["register"],
	}
	return render(request, 'auth_form.html', context)

def auth_logout(request):
	logout(request)
	messages.success(request, 'Success, you are now logged out')
	return render(request, 'index.html')

def auth_register(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect("/")

	form = RegisterForm(request.POST or None)
	if form.is_valid():
		new_user = MyUser.objects.create_user(email=form.cleaned_data['email'],
			password=form.cleaned_data["password2"],
			first_name=form.cleaned_data['firstname'], last_name=form.cleaned_data['lastname'],
    		is_student=form.cleaned_data['student'], is_professor=form.cleaned_data['professor'],
    		is_engineer=form.cleaned_data['engineer'])
		new_user.save()
		login(request, new_user);
		messages.success(request, 'Success! Your account was created.')
		return render(request, 'index.html')

	context = {
		"form": form,
		"page_name" : "Register",
		"button_value" : "Register",
		"links" : ["login"],
	}
	return render(request, 'auth_form.html', context)

@login_required
def update_profile(request):
	global target_user
	if target_user != None :
		request.user = target_user

	if request.user.is_professor == True:
		form = UpdateProfessorForm(request.POST or None, instance=request.user)
	elif request.user.is_engineer == True:
		form = UpdateEngineersForm(request.POST or None, instance=request.user)
	elif request.user.is_student == True:
		form = UpdateStudentForm(request.POST or None, instance=request.user)
	else:
		form = UpdateForm(request.POST or None, instance=request.user)

	if form.is_valid():
		form.save()
		target_user = None
		messages.success(request, 'Success, your profile was saved!')

	context = {
		"form": form,
		"page_name" : "Update",
		"button_value" : "Update",
		"links" : ["logout"],
	}
	return render(request, 'auth_form.html', context)


@login_required
def update_handler(request):
	global target_user
	target = request.POST.get('target_user',None);
	target_user = MyUser.objects.get(email__exact=target)
	logging.getLogger('django').info(target_user)
	return redirect('/update',request)


@login_required
def get_profile(request):
	in_name = request.GET.get('name', 'None')
	if in_name == None:
		in_name = request.POST.get('name', 'None')

	try:
		profile_User = MyUser.objects.get(email__exact=in_name)
	except:
		return render(request, 'not_found.html')

	if profile_User.get_email == request.user.get_email or request.user.is_admin == True:
		context = {'currUser' : profile_User, 'updatePermission' : True,}
	else:
		context = {'currUser' : profile_User, 'updatePermission' : False,}


	if profile_User.is_professor == True:
		return render(request, 'professor_profile.html',context)

	elif profile_User.is_engineer == True:
		return render(request, 'engineers_profile.html',context)

	elif profile_User.is_student == True:
		return render(request, 'student_profile.html',context)

	elif profile_User.is_admin == True:
		return render(request, 'admin_profile.html',context)
	else:
		return render(request, 'not_found.html')
