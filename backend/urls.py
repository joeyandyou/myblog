from django.conf.urls import url
from backend import views

urlpatterns = [
    url(r'^$', views.index),

    url(r'^login$', views.login),
    url(r'^logout$', views.logout),

    url(r'^banner/list$', views.banner_list),
    url(r'^banner/form$', views.banner_form),
    url(r'^banner/delete$', views.banner_delete),
]
