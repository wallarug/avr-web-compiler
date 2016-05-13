from django.conf.urls import url

#from . import views


from views import *

urlpatterns = [
    url(r'^$', DashboardView.as_view(), name='dashboard'),
    #url(r'^', CompileView.as_view()),
    url(r'^files/$', FileList.as_view(), name='list code'),
    url(r'^files/$', CreateProgramView.as_view(), name='new code'),
    url(r'^files/$', FileList.as_view(), name='files'),
    #url(r'^files/(?P<pk>\d+)/$', FileView.as_view()),
    #url(r'^file/$', FileView.as_view(), name='file'),
]

