# Create your views here.
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponse

from django.views.generic import ListView, DetailView, View
from django.template import RequestContext

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import time

import subprocess
from django.core.files import File
import serial

from braces.views import LoginRequiredMixin


class CompileView(LoginRequiredMixin,View):
    template_name = 'avrcompiler/main.html'

    def get(self, request, *args, **kwargs):
	data = {}
	if args:
		print "Has KWARGS!"
		data = args['data']
        return render_to_response(self.template_name, RequestContext(request, data))
        #return HttpResponse("G'day, What you are trying to do is not right.")

    def post(self, request, *args, **kwargs):
        data = {}
	code = self.request.POST.get('code')
	data['code'] = code
	
	code_file = open('avrcompiler/program.s', 'w')
	myFile = File(code_file)
	myFile.write(code)
	myFile.close()

	message = subprocess.check_output(["bash", "avrcompiler/compile_upload.sh", "avrcompiler/program.s"])
	arr = message.split('\n')
	data['message'] = arr
	try:
		ser = serial.Serial("/dev/ttyACM0", 9600, timeout=3)
		tdata = ser.read()           # Wait forever for anything
		time.sleep(1)              # Sleep (or inWaiting() doesn't give the correct value)
		data_left = ser.inWaiting()  # Get the number of characters ready to be read
		tdata += ser.read(data_left) # Do the read and combine it with the first character
	finally:
		ser.close()
		data['console'] = tdata
        return render_to_response(self.template_name, RequestContext(request, data))

class FileView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
	print "Running get..."
	data = {}
	codeFile = 'avrcompiler/saved_code/'+str(self.request.POST.get('file'))
	method = self.request.POST.get('type')
	code = self.request.POST.get('code')
	print codeFile, method, code
	if method == '0':
		# Save File
		dataFile = open(codeFile, 'w')
		myFile = File(dataFile)
		myFile.write(code)
		myFile.close()
	if method == '1':
		# Load File
		try:
			dataFile = open(codeFile, 'r')
			myFile = File(dataFile)
			data['code'] = myFile.readlines()
			myFile.close()
		except:
			data['errormessage'] = "File not found."
			
	return HttpResponseRedirect(reverse('compiler'))

## THEIFED FRoM AUDIENCE PRECISION
## https://github.com/stefanfoulis/django-class-based-auth-views
    # Login / Logout views

try:
    import urlparse
except ImportError:
    from urllib import parse as urlparse # python3 support
from class_based_auth_views.utils import default_redirect
from django.contrib.auth import REDIRECT_FIELD_NAME, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, resolve_url
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic import View
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.edit import FormView
from django.conf import settings


class LoginView(FormView):
    """
    This is a class based version of django.contrib.auth.views.login.
    Usage:
        in urls.py:
            url(r'^login/$',
                LoginView.as_view(
                    form_class=MyCustomAuthFormClass,
                    success_url='/my/custom/success/url/),
                name="login"),
    """
    form_class = AuthenticationForm
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'registration/login.html'
    success_url = '/'

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        """
        The user has provided valid credentials (this was checked in AuthenticationForm.is_valid()).
        """
        self.request.session['username'] = form.get_user().username
        # self.request.session['access_token'] = self.data['access_token']
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)

    def form_invalid(self, form):
        """
        The user has provided invalid credentials (this was checked in AuthenticationForm.is_valid()).
        """
        return super(LoginView, self).form_invalid(form)

    def get_success_url(self):
        if self.success_url:
            redirect_to = self.success_url
        else:
            redirect_to = self.request.GET.get(self.redirect_field_name, '')

        netloc = urlparse.urlparse(redirect_to)[1]
        if not redirect_to:
            redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)
        # Security check -- don't allow redirection to a different host.
        elif netloc and netloc != self.request.get_host():
            redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)
        return redirect_to


    def get(self, request, *args, **kwargs):
        """
        Same as django.views.generic.edit.ProcessFormView.get()
        """
        return super(LoginView, self).get(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        """
        Same as django.views.generic.edit.ProcessFormView.post(), but adds test cookie stuff
        """
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class LogoutView(TemplateResponseMixin, View):
    template_name = "registration/logout.html"
    redirect_field_name = "next"

    def get(self, request, *args, **kwargs):
        logout(request)
        context = self.get_context_data()
        response = self.render_to_response(context)
        return response

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            logout(self.request)
        return redirect(self.get_redirect_url())

    def get_context_data(self, **kwargs):
        context = kwargs
        redirect_field_name = self.get_redirect_field_name()
        context.update({
            "redirect_field_name": redirect_field_name,
            "redirect_field_value": self.request.GET.get(redirect_field_name),
            })
        return context

    def get_redirect_field_name(self):
        return self.redirect_field_name

    def get_redirect_url(self, fallback_url=None, **kwargs):
        if fallback_url is None:
            fallback_url = settings.LOGIN_URL
        kwargs.setdefault("redirect_field_name", self.get_redirect_field_name())
        response = default_redirect(self.request, fallback_url, **kwargs)
        return response
