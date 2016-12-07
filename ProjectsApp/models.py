"""ProjectsApp Models

Created by Harris Christiansen on 10/02/16.
"""
from django.db import models
import logging
import datetime
from AuthenticationApp.models import MyUser

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=10000)
    created_at = models.DateTimeField('date created')
    updated_at = models.DateTimeField('date updated')
    owner =  models.ForeignKey('AuthenticationApp.MyUser', related_name='Engineer', null=True, blank=True)
    company = models.ForeignKey('CompaniesApp.Company', null=True, blank=True)
    programmingLanguage = models.CharField(max_length=200,null=True, blank=True)
    yearsOfExperience = models.CharField(max_length=200,null=True, blank=True)
    speciality = models.CharField(max_length=200,null=True, blank=True)
    bookers = models.ManyToManyField(MyUser)
    def __str__(self):
        return self.name

    def create_project(self, name=None, description=None, programmingLanguage=None, yearsOfExperience=None, speciality=None, owner=None, company=None):
        if not name:
            return ValueError('Project has to have a name')
        logging.getLogger('django').info("here")
        self.name = name
        self.description = description
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        self.owner = owner
        self.company = company
        self.save()
        return

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_created_at(self):
        return self.created_at

    def get_updated_at(self):
        return self.updated_at

    def get_owner(self):
        return self.owner

    def get_company(self):
        return self.company

    def get_programmingLanguage(self):
        return self.programmingLanguage

    def get_yearsOfExperience(self):
        return self.yearsOfExperience

    def get_speciality(self):
        return self.speciality

    def get_members(self):
        return self.members

    def __self__(self):
        return self.name

    def __unicode(self):
        return self.name
