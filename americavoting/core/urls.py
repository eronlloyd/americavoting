from django.conf.urls import url


from . import views

urlpatterns = [
    url(r'^$', views.division_index, name='division_index'),
    url(r'^([a-z]+)/$', views.division_detail, name='division_detail'),
]
