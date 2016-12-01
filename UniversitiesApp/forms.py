"""
UniversitiesApp Forms

Created by Jacob Dunbar on 11/5/2016.
"""
from django import forms
from .models import University

class UniversityForm(forms.ModelForm):
    class Meta:
        model = University
        fields = ('name', 'photo', 'description', 'website')
    
        def clean_name(self):
            return self.cleaned_data.get('name')

        def clean_photo(self):
            return self.cleaned_data.get('photo')

        def clean_desc(self):
            return self.cleaned_data.get('description')

        def clean_website(self):
            return self.cleaned_data.get('website')

    #name = forms.CharField(label='Name', max_length=50)
    #photo = forms.ImageField(label='Photo')
    #description = forms.CharField(label='Description', max_length=300)
    #website = forms.CharField(label='Website', max_length = 300)
	
class CourseForm(forms.Form):
	tag = forms.CharField(label='Tag', max_length=10)
	name = forms.CharField(label='Name', max_length=50)
	description = forms.CharField(label='Description', max_length=300)

class UniForm(forms.Form):
    name = forms.CharField(label='Name', max_length=50)
    univName = forms.CharField(label='univName', max_length=60)
    cName = forms.CharField(label='tag', max_length=10)
