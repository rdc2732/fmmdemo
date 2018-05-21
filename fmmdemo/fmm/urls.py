from django.conf.urls import url

from . import views
app_name = 'fmm'
urlpatterns = [
    url('^$', views.index, name='index'),
    url('^(?P<group_number>[0-9]+)/$', views.GroupFunctionList.as_view(), name='group_list'),
    url('^(?P<group_number>[0-9]+)/(?P<function_number>[0-9]+)/$', views.FunctionFeatureList.as_view(), name='function_list'),
    url('^groups', views.GroupList.as_view()),
    url('^functions', views.FunctionList.as_view()),
    url('^features', views.FeatureList.as_view()),
    url('^loadfmm', views.loadfmm, name='loadfmm'),
]