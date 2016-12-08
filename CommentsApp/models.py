from __future__ import unicode_literals
from django.db import models
from AuthenticationApp.models import MyUser

class Token(models.Model):
    token = models.CharField(max_length=10)

# Create your models here.
class Comment(models.Model):
    token = models.ForeignKey('Token', null=True, blank=True)
    time = models.DateTimeField(auto_now=True)
    comment = models.CharField(max_length=500)
    group = models.ForeignKey('GroupsApp.Group', null=True, blank=True)
    user = models.ForeignKey(MyUser, null=True, blank=True)
