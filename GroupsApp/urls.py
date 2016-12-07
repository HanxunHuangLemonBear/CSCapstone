"""GroupsApp URL

Created by Naman Patwari on 10/10/2016.
"""
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^group/all$', views.getGroups, name='Groups'),
    url(r'^group/addMemberForm$', views.addMemberForm, name='GroupAddMember'),
    url(r'^group/AddMemberFormSuccess$', views.addMemberFormSuccess, name='GroupAddMemberSuccess'),
    url(r'^group/addcomment$', views.addComment, name="GroupComment"),
    url(r'^group/deletegroupform$', views.deleteGroupForm, name='GroupDelete'),
    url(r'^group/deletegroupformsuccess$', views.deleteGroupFormSuccess, name='GroupDeleteSuccess'),
	url(r'^group/form$', views.getGroupForm, name='GroupForm'),
    url(r'^group/formsuccess$', views.getGroupFormSuccess, name='GroupFormSuccess'),
    url(r'^group/join$', views.joinGroup, name='GJoin'),
    url(r'^group/setprojectform$', views.setProjectForm, name='GSetProject'),
    url(r'^group/setprojectformsuccess$', views.setProjectFormSuccess, name='GSetProjectSuccess'),
    url(r'^group/unjoin$', views.unjoinGroup, name='GUnjoin'),
    url(r'^group/addTag$', views.addTag, name='addTag'),
    url(r'^group/removeTag$', views.removeTag, name='removeTag'),
    url(r'^group$', views.getGroup, name='Group'),
]
