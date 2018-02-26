from django.conf.urls import url
from . import views
urlpatterns = [
	url(r'^$', views.index),
	url(r'^signin$', views.signin),
	url(r'^register$', views.register),
	url(r'^reg$', views.reg),
	url(r'^login$', views.login),
	url(r'^dashboard$', views.dashboard),
	url(r'^logout$', views.logout),
	url(r'^users/edit$', views.edit),
	url(r'^editinfo$', views.editinfo),
	url(r'^editpword$', views.editpword),
	url(r'^editdesc$', views.editdesc),
	url(r'^users/edit/(?P<uid>\d+)$', views.edituser),
	url(r'^adduser$', views.adduser)

]