"""reference URL Configuration

This application level URL.PY file is called via the project level URL.PY file.

"""
from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^register$', views.register),
	url(r'^login$', views.login),
	url(r'^logout$', views.logout),
	url(r'^edit$', views.edit),
	url(r'^saveedit$', views.saveEdit),
]