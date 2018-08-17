from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.loginReg),
    url(r'^login_process$', views.login_process),
    url(r'^reg_process$', views.reg_process),
    url(r'^success$', views.success)
]