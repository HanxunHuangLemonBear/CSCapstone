"""AuthenticationApp URL Configuration

Created by Naman Patwari on 10/4/2016.
"""

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login$', views.auth_login, name='Login'),
    url(r'^logout$', views.auth_logout, name='Logout'),
    url(r'^register$', views.auth_register, name='Register'),
    url(r'^update$', views.update_profile, name='UpdateProfile'),
    url(r'^profile$', views.get_profile, name='Profile'),
    url(r'^update_handler$', views.update_handler, name='Update_handler'),

]
