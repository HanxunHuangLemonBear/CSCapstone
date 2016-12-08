"""GroupsApp Models

Created by Naman Patwari on 10/10/2016.
"""
from django.db import models
from AuthenticationApp.models import MyUser
from ProjectsApp.models import Project
from CommentsApp.models import Comment
from CommentsApp.models import Token
# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    members = models.ManyToManyField(MyUser)
    project_name = models.ForeignKey('ProjectsApp.Project', null=True, blank=True)
    tag = models.ManyToManyField('ProjectsApp.projectTag', blank=True)

    def __str__(self):
        return self.name
