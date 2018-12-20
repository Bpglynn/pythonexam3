"""reference URL Configuration

This application level URL.PY file is called via the project level URL.PY file.

"""
from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^postquote$', views.postQuote),
	url(r'^deletequote/(?P<number>\d+)$', views.deleteQuote),
	url(r'^user/(?P<number>\d+)$', views.viewUser),
	url(r'^like/(?P<number>\d+)$', views.likeQuote),
]