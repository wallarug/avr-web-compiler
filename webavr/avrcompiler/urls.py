from django.conf.urls import url

#from . import views

from views import CompileView, LoginView, LogoutView, RegisterView, FileListView, FileView

urlpatterns = [
    url(r'^$', CompileView.as_view(), name='compiler'),
    #url(r'^', CompileView.as_view()),
    url(r'^files/$', FileListView.as_view(), name='files'),
    url(r'^files/(?P<pk>\d+)/$', FileView.as_view()),
    url(r'^file/$', FileView.as_view(), name='file'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(),  name='logout'),
    url(r'^register/$', RegisterView.as_view(),  name='register'),
]
