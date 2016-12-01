"""
UniversitiesApp Models

Created by Jacob Dunbar on 11/5/2016.
"""
from django.db import models
from AuthenticationApp.models import MyUser
from tinymce.models import HTMLField

# Create your models here.
class University(models.Model):
    name = models.CharField(max_length=50)
    photo = models.ImageField(upload_to="static/universityimages", default=0)
    description = models.CharField(max_length=300)
    website=models.CharField(max_length=300, default="/")
    members = models.ManyToManyField(MyUser)

    def get_name(self):
        return self.name

    def get_photo(self):
        return self.photo

    def get_desc(self):
        return self.description

    def get_web(self):
        return self.website

    def get_members(self):
        return self.members

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

class Course(models.Model):
	tag = models.CharField(max_length=10)
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=300)
	university = models.ForeignKey(University, on_delete=models.CASCADE)
	members = models.ManyToManyField(MyUser)

	def __str__(self):
		return self.name
