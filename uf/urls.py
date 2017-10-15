from django.conf.urls import url
from . import views

app_name  = 'uf'

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^list$', views.listUfHistory, name = 'list'),
    url(r'^price$', views.price, name = 'price'),
    url(r'^retrieveUF$', views.retrieveUF, name = 'retrieveUF'),
    url(r'^clearDB$', views.clearDB, name = 'clearDB'),
]
