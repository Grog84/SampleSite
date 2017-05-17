from django.conf.urls import url
from . import views

app_name = 'sample'

urlpatterns = [
    url(r'^home/$', views.index, name='index'),

    url(r'^Logout/$', views.LogoutView.as_view(), name='logout'),

    url(r'^Sets/$', views.sets, name='sets'),

    url(r'^Sets/(?P<sampleset_id>[0-9]+)/$', views.set_detail, name='set_detail'),

    url(r'^Samples/$', views.samples, name='samples'),

    url(r'^Samples/(?P<sample_id>[0-9]+)/$', views.sample_detail, name='sample_detail'),

    url(r'Sets/add/', views.SampleSetCreate.as_view(), name='set_add'),

    url(r'Sets/edt/(?P<pk>[0-9]+)/$', views.SampleSetUpdate.as_view(), name='set_update'),

    url(r'Sets/edt/(?P<sampleset_id>[0-9]+)/delete/$', views.SampleSetDelete.as_view(), name='set_delete'),

    url(r'Sample/add/', views.SampleCreate.as_view(), name='sample_add'),
]
