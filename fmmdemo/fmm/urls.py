from django.conf.urls import url

from . import views
app_name = 'fmm'
urlpatterns = [
    url('^$', views.index, name='index'),
    url('^(?P<group_number>[0-9]+)/$', views.GroupFunctionList.as_view(), name='group_list'),
    url('^(?P<group_number>[0-9]+)/(?P<function_number>[0-9]+)/$', views.FunctionFeatureList.as_view(), name='function_list'),
    url('^groups', views.GroupList.as_view()),
    url('^functions', views.FunctionList.as_view()),
    url('^testfeatures', views.TestFeatureList.as_view()),
    url('^features', views.FeatureList.as_view()),
    url('^dependency', views.DependencyList.as_view()),
    url('^loadfmm', views.loadfmm, name='loadfmm'),
    url('^yourname',views.get_name, name='getname'),
    url('^test', views.test, name='test'),
    url(r'^feature/(?P<feature_number>[0-9]+)/$', views.edit_feature, name="edit_feature"),
    url(r'^fmm_main/$', views.fmm_main_index, name="main_index"),
    url(r'^fmm_main/(?P<group_number>[0-9]+)/$', views.fmm_main, name="fmm_main"),
]
