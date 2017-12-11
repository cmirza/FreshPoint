from django.conf.urls import url
from . import views

app_name = 'FreshPoint'
urlpatterns = [
    url(r'^$', views.index, name='index'),
]
