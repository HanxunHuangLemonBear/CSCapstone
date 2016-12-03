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
		context = {'currProject' : currProject}
		if request.user.is_admin == True or request.user == currProject.owner or request.user.company_name == currProject.company:
			context.update({'deletePermission' : True})
		if request.user == currProject.owner:
			context.update({'updatePermission' : True})
		return render(request, 'project.html',context)
	except:
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
