"""ProjectsApp Views

Created by Harris Christiansen on 10/02/16.
"""
from django.shortcuts import render
from django.db.models import Max
from . import models
from . import forms
import datetime
import logging
from .models import Project
from .forms import ProjectForm
from AuthenticationApp.models import MyUser


def getProjects(request):
	projects_list = models.Project.objects.all()
	return render(request, 'projects.html', {
        'projects': projects_list,
    })

def getProject(request):
	project_name = request.GET.get("name",None)
	if project_name == None:
		return render(request, 'not_found.html')
	try:
		currProject = models.Project.objects.get(name__exact=project_name)
                isBookmark = request.user.project_set.filter(name__exact=project_name).exists()
                context = {'currProject' : currProject,
                           'isBookmark'  : isBookmark,        
                }
		if request.user.is_admin == True or request.user == currProject.owner or request.user.company_name == currProject.company:
			context.update({'deletePermission' : True})
		if request.user == currProject.owner:
			context.update({'updatePermission' : True})
		return render(request, 'project.html',context)
	except:
                print("B")
		return render(request, 'not_found.html')

def getProjectForm(request):
	if request.user.is_authenticated():
		if not request.user.is_engineer:
			return render(request, 'projectform.html', {'user_error' : 'Only Engineers can create_project'})
		return render(request, 'projectform.html')
    # render error page if user is not logged in
	return render(request, 'autherror.html')

def getProjectFormSuccess(request):
	if request.user.is_authenticated():
		if not request.user.is_engineer:
			return render(request, 'projectform.html', {'user_error' : 'Only Engineers can create_project'})

		if request.method == 'POST':
			form = forms.ProjectForm(request.POST, request.FILES)
			if form.is_valid():
				if models.Project.objects.filter(name__exact=form.cleaned_data['name']).exists():
					return render(request, 'projectform.html', {'error' : 'Error: That project name already exists!'})
				new_project = Project()
				new_project.create_project(
					name=form.cleaned_data.get('name',None),
					description=form.cleaned_data.get('description',None),
					programmingLanguage=form.cleaned_data.get('programmingLanguage',None),
					yearsOfExperience=form.cleaned_data.get('yearsOfExperience',None),
					speciality=form.cleaned_data.get('speciality',None),
					owner=request.user,
					company=request.user.company_name
				)
				context = {'name' : form.cleaned_data['name'],}
				return render(request, 'projectformsuccess.html', context)

		else:
			form = forms.ProjectForm()
	return render(request, 'projectform.html')

def makeBookmark(request):
    if request.user.is_authenticated():
        in_pName = request.GET.get('pname', 'None')
        in_email = request.user.email
        print(in_email)
        in_user = models.MyUser.objects.get(email__exact=in_email)
        currProject = models.Project.objects.get(name__exact=in_pName)
        print(currProject)
        in_user.project_set.add(currProject)
	in_user.save()
        context = {'currProject' : currProject,
                   'isBookmark'  : True,
                }
	if request.user.is_admin == True or request.user == currProject.owner or request.user.company_name == currProject.company:
	    context.update({'deletePermission' : True})
	if request.user == currProject.owner:
	    context.update({'updatePermission' : True})
        return render(request, 'project.html', context)
    return render(request, 'not_found.html')

def removeBookmark(request):
    if request.user.is_authenticated():
        in_pName = request.GET.get('pname', 'None')
        in_email = request.user.email
        in_user = models.MyUser.objects.get(email__exact=in_email)
        currProject = models.Project.objects.get(name__exact=in_pName)
        in_user.project_set.remove(currProject)
	in_user.save()
        context = {'currProject' : currProject,
                   'isBookmark'  : False,
                }
	if request.user.is_admin == True or request.user == currProject.owner or request.user.company_name == currProject.company:
	    context.update({'deletePermission' : True})
	if request.user == currProject.owner:
	    context.update({'updatePermission' : True})
        return render(request, 'project.html', context)
    return render(request, 'not_found.html')

def delete_handler(request):
	currProject_name = request.POST.get('target_project',None)
	try:
		currProject = models.Project.objects.get(name__exact=currProject_name)
	except:
		return render(request, 'not_found.html')


	if request.user.is_admin == False and request.user != currProject.owner and request.user.company_name != currProject.company:
		context = {'error' : "You do not have no permission to delete this project",'is_error':True,'currProject':currProject}
		return render(request, 'project.html',context)

	currProject.delete()
	context = {'name' : currProject_name}
	return render(request, 'projectdeleteformsuccess.html',context)


def update_handler(request):
	currProject_name = request.POST.get('target_project',None)
	try:
		currProject = models.Project.objects.get(name__exact=currProject_name)
	except:
		return render(request, 'not_found.html')

	if request.user.is_admin == False and request.user != currProject.owner:
		context = {'error' : "You do not have no permission to delete this project",'is_error':True,'currProject':currProject}
		return render(request, 'project.html',context)
	context = {'currProject' : currProject}
	form = forms.ProjectForm(request.POST)
	context.update({'form':form})
	return render(request, 'updateform.html',context)

def update(request):
	if request.method == 'POST':
		form = forms.ProjectForm(request.POST, request.FILES)
		if form.is_valid():
			logging.getLogger('django').info(request.user)
			try:
				currProject = models.Project.objects.get(name__exact=form.cleaned_data['name'])
			except:
				return render(request, 'not_found.html')
			currProject.programmingLanguage = form.cleaned_data['programmingLanguage']
			currProject.yearsOfExperience = form.cleaned_data['yearsOfExperience']
			currProject.speciality = form.cleaned_data['speciality']
			currProject.description = form.cleaned_data['description']
			currProject.save()
			context = {'name' : form.cleaned_data['name'],}
			return render(request, 'projectformsuccess.html', context)
	else:
		#logging.getLogger('django').info(request.user)
		form = forms.ProjectForm()
	return render(request, 'updateform.html')
