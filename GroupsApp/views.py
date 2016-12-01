"""GroupsApp Views
Created by Naman Patwari on 10/10/2016.
"""
from django.shortcuts import render

from . import models
from . import forms

def getGroups(request):
    if request.user.is_authenticated():
        groups_list = models.Group.objects.all()
        context = {
            'groups' : groups_list,
        }
        return render(request, 'groups.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getGroup(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_group = models.Group.objects.get(name__exact=in_name)
        is_member = in_group.members.filter(email__exact=request.user.email)
        comments_list = models.Comment.objects.all()
        context = {
            'comments' : comments_list,
            'group' : in_group,
            'userIsMember': is_member,
        }
        return render(request, 'group.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getGroupForm(request):
    if request.user.is_authenticated():
        return render(request, 'groupform.html')
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getGroupFormSuccess(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = forms.GroupForm(request.POST)
            if form.is_valid():
                if models.Group.objects.filter(name__exact=form.cleaned_data['name']).exists():
                    return render(request, 'groupform.html', {'error' : 'Error: That Group name already exists!'})
                new_group = models.Group(name=form.cleaned_data['name'], description=form.cleaned_data['description'])
                new_group.save()
                context = {
                    'name' : form.cleaned_data['name'],
                }
                return render(request, 'groupformsuccess.html', context)
        else:
            form = forms.GroupForm()
        return render(request, 'groupform.html')
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def joinGroup(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_group = models.Group.objects.get(name__exact=in_name)
        in_group.members.add(request.user)
        in_group.save();
        request.user.group_set.add(in_group)
        request.user.save()
        context = {
            'group' : in_group,
            'userIsMember': True,
        }
        return render(request, 'group.html', context)
    return render(request, 'autherror.html')

def unjoinGroup(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_group = models.Group.objects.get(name__exact=in_name)
        in_group.members.remove(request.user)
        in_group.save();
        request.user.group_set.remove(in_group)
        request.user.save()
        context = {
            'group' : in_group,
            'userIsMember': False,
        }
        return render(request, 'group.html', context)
    return render(request, 'autherror.html')

def addMemberForm(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_group = models.Group.objects.get(name__exact=in_name)
        context = {
            'name' : in_name,
            'group' : in_group,
            'userIsMember': True,
        }
        return render(request, 'addMemberForm.html', context)


def addMemberFormSuccess(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = forms.AddMemberForm(request.POST, request.FILES)
            if form.is_valid():
                in_email = form.cleaned_data['email']
                user = models.MyUser.objects.get(email__exact=in_email)
                in_name = form.cleaned_data['group_name']
                in_group = models.Group.objects.get(name__exact=in_name)
                print(in_name)
                in_group.members.add(user)
                in_group.save();
                user.group_set.add(in_group)
                user.save()
                context = {
                    'group' : in_group,
                    'userIsMember' : True
                }
                return render(request, 'group.html', context)
            else:
                return render(request, 'groups.html')
    return render(request, 'autherror.html')


def setProjectForm(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_group = models.Group.objects.get(name__exact=in_name)
        context = {
            'name' : in_name,
            'group' : in_group,
            'userIsMember': True,
        }
        return render(request, 'groupsetprojectform.html', context)

def setProjectFormSuccess(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = forms.SetGroupProjectForm(request.POST, request.FILES)
            if form.is_valid():
                in_projectname = form.cleaned_data['project_name']
                in_project = models.Project.objects.get(name__exact=in_projectname)
                in_name = form.cleaned_data['group_name']
                in_group = models.Group.objects.get(name__exact=in_name)
                in_group.project.add(in_project)
                in_group.save();
                context = {
                    'group' : in_group,
                    'userIsMember' : True
                }
                return render(request, 'group.html', context)
            else:
                return render(request, 'groups.html')
    return render(request, 'autherror.html')

def deleteGroupForm(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_group = models.Group.objects.get(name__exact=in_name)
        context = {
            'name' : in_name,
            'group' : in_group,
            'userIsMember': True,
        }
        return render(request, 'groupdelete.html', context)

def deleteGroupFormSuccess(request):
    if request.user.is_authenticated():
        groups_list = models.Group.objects.all()
        context = {
            'groups' : groups_list,
        }
        if request.method == 'POST':
            form = forms.DeleteGroupForm(request.POST, request.FILES)
            if form.is_valid():
                in_confirm = form.cleaned_data['confirm']
                in_name = form.cleaned_data['group_name']
                in_group = models.Group.objects.get(name__exact=in_name)

                if(in_confirm == 'confirm'):
                    for user in in_group.members.all():
                        in_group.members.remove(user)
                        in_group.save();
                        user.group_set.remove(in_group)
                        user.save()
                        in_group.delete()
                    return render(request, 'groups.html', context)
                else:
                    context = {
                        'name' : in_name,
                        'group' : in_group,
                        'userIsMember' : True
                    }
                    return render(request, 'group.html', context)
                #return render(request, 'groups.html')
            else:
                return render(request, 'groups.html',context)
    return render(request, 'autherror.html')

def addComment(request):
    if request.method == 'POST':
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            in_name = form.cleaned_data['group_name']
            in_group = models.Group.objects.get(name__exact=in_name)
            new_comment = models.Comment(comment=form.cleaned_data['description'])
            new_comment.save()
            comments_list = models.Comment.objects.all()
            context = {
                'comments' : comments_list,
                'name' : in_name,
                'group' : in_group,
                'userIsMember' : True
            }
            return render(request, 'group.html', context)
        else:
            form = forms.CommentForm()
            in_name = form.cleaned_data['group_name']
            in_group = models.Group.objects.get(name__exact=in_name)
            new_comment = models.Comment(comment=form.cleaned_data['description'])
            new_comment.save()
            comments_list = models.Comment.objects.all()
            context = {
                'comments' : comments_list,
                'name' : in_name,
                'group' : in_group,
                'userIsMember' : True
            }
    return render(request, 'group.html', context)
