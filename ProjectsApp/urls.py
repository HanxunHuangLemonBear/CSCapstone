"""ProjectsApp URL Configuration

Created by Harris Christiansen on 10/02/16.
"""
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^project/all$', views.getProjects, name='Projects'),
    url(r'^project$', views.getProject, name='Project'),
    url(r'^project/create$', views.getProjectForm, name='createProject'),
    url(r'^project/formsuccess$', views.getProjectFormSuccess, name='ProjectFormSuccess'),
    url(r'^project/delete_handler$', views.delete_handler, name='deleteHandler'),
    url(r'^project/update_handler$', views.update_handler, name='updateHandler'),
    url(r'^project/update$', views.update, name='updateHandler'),
    url(r'^project/bookmark$', views.makeBookmark, name='makeBookmark'),
    url(r'^project/bookmark/remove$', views.removeBookmark, name='removeBookmark'),
    url(r'^project/addTag$', views.addTag, name='addTag'),
    url(r'^project/removeTag$', views.removeTag, name='removeTag'),
]
