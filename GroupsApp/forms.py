"""GroupsApp Forms

Created by Naman Patwari on 10/10/2016.
"""
from django import forms

class GroupForm(forms.Form):
    name = forms.CharField(label='Name', max_length=30)
    description = forms.CharField(label='Description', max_length=300)
    project = None

class AddMemberForm(forms.Form):
    email = forms.CharField(label='Email', max_length=30)
    group_name = forms.CharField(label='GroupName', max_length=30)

class SetGroupProjectForm(forms.Form):
    project_name = forms.CharField(label="Name", max_length=30)
    group_name = forms.CharField(label='GroupName', max_length=30)

class DeleteGroupForm(forms.Form):
    confirm = forms.CharField(label="Confirm", max_length=30)
    group_name = forms.CharField(label='GroupName', max_length=30)

class CommentForm(forms.Form):
    group_name = forms.CharField(label='GroupName', max_length=30)
    description = forms.CharField(label='Text', max_length=500)

class CommentDeleteForm(forms.Form):
    group_name = forms.CharField(label='GroupName', max_length=30)
    token = forms.CharField(label='Token', max_length=10)
