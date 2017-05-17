from django.conf.urls import url
from django.contrib.auth.views import login
from . import views

app_name = 'signin'

urlpatterns = [
    url(r'^$', login, name='login'),
    ]