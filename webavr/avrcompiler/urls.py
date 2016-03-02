from django.conf.urls import url

#from . import views

<<<<<<< HEAD
from views import CompileView, FileView

urlpatterns = [
    url(r'^$', CompileView.as_view(), name='compiler'),
    url(r'^files/$', FileView.as_view(), name='files'),
=======
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
>>>>>>> 1df3c1dc3071a3fd5e0533c994489afcc873c387
]
