from django.conf.urls import url

#from . import views

from views import CompileView, FileView

urlpatterns = [
    url(r'^$', CompileView.as_view(), name='compiler'),
    url(r'^files/$', FileView.as_view(), name='files'),
]
