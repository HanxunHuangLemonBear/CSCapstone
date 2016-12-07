"""
CompaniesApp Forms

Created by Jacob Dunbar on 10/3/2016.
"""
from django import forms
from .models import Project

class ProjectForm(forms.Form):
    name = forms.CharField(label='Name', max_length=30)
    description = forms.CharField(label='Description', max_length=300)
    programmingLanguage = forms.CharField(label='programmingLanguage', max_length = 300)
    speciality = forms.CharField(label='speciality', max_length = 300)
    yearsOfExperience = forms.CharField(label='speciality', max_length = 300)
    class Meta:
        model = Project
        fields = ('name', 'programmingLanguage', 'description', 'speciality','yearsOfExperience','tag')

        def clean_name(self):
            return self.cleaned_data.get('name')

        def clean_programmingLanguage(self):
            return self.cleaned_data.get('programmingLanguage')

        def clean_desc(self):
            return self.cleaned_data.get('description')

        def clean_speciality(self):
            return self.cleaned_data.get('speciality')

        def clean_yearsOfExperience(self):
            return self.cleaned_data.get('yearsOfExperience')

        def clean_tag(self):
            return self.cleaned_data.get('tag')
