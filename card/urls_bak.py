from django.conf import settings
from django.conf.urls import url,include
from . import views

urlpatterns = [
    url(r'^$', views.home, name="home_page"),
    url(r'^nalanda/$', views.home2, name="home_page"),
    url(r'^nalanda/(?P<cl>\d+)/$', views.viewnalanda, name='nalanda'),
    url(r'^(?P<cl>\d+)/$', views.reportcard, name='reportcard'),
]
