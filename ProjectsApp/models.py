"""ProjectsApp Models

Created by Harris Christiansen on 10/02/16.
"""
from django.db import models
import logging

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=10000)
    created_at = models.DateTimeField('date created')
    updated_at = models.DateTimeField('date updated')
    owner =  models.ForeignKey('AuthenticationApp.MyUser', null=True, blank=True)
    company = models.ForeignKey('CompaniesApp.Company', null=True, blank=True)
    programmingLanguage = models.CharField(max_length=200,null=True, blank=True)
    yearsOfExperience = models.CharField(max_length=200,null=True, blank=True)
    speciality = models.CharField(max_length=200,null=True, blank=True)

    def __str__(self):
        return self.name

    def create_project(self, name=None, description=None, programmingLanguage=None, yearsOfExperience=None, speciality=None):
        if not name:
            return ValueError('Project has to have a name')
        logging.getLogger('django').info("here")
        new_project = self.model(name=name)
        new_project.description = description
        new_project.created_at = datetime.now()
        #new_project.save()
        return
