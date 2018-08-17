from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.loginReg),
    url(r'^login_process$', views.login_process),
    url(r'^reg_process$', views.reg_process),
    url(r'^quotes$', views.quotes),
    url(r'^logout$', views.logout),
    url(r'^myaccount/(?P<num>\d+)$', views.edit),
    url(r'^update$', views.update),
    url(r'^user/(?P<num>\d+)$', views.user),
    url(r'^like/(?P<num>\d+)$', views.like),
    url(r'^add_quote$', views.add_quote),
    url(r'^delete/(?P<num>\d+)$', views.delete)


]