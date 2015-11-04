from django.conf.urls import url

#from . import views

from views import CompileView, LoginView, LogoutView, FileView

urlpatterns = [
    url(r'^$', CompileView.as_view(), name='compiler'),
    url(r'^files/$', FileView.as_view(), name='files'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(),  name='logout'),
]
