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
from .models import AssemblyProgram

class CompileView(LoginRequiredMixin,View):
    template_name = 'avrcompiler/main.html'

    def get(self, request, *args, **kwargs):
        data = {}
        try:
            errors = request.session['errors']
            data['errormessage'] = errors
        except KeyError:
            pass
        try:
            sesh = request.session['program']
            data['code'] = sesh['code']
            data['name'] = sesh['name']
            data['id'] = sesh['id']
            del request.session['program']
        except KeyError:
            program = AssemblyProgram.objects.get(name='template')
            data['name'] = "template"
            data['code'] = program.getCode()
            data['id'] = None
        return render_to_response(self.template_name, RequestContext(request, data))

    def post(self, request, *args, **kwargs):
        data = {}
        code = request.POST.get('code')
        name = request.POST.get('progname')
        id = request.POST.get('progid')

        print name
        print id

        data['code'] = code
        data['name'] = name
        data['id'] = id
        data['console'] = ''

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

class FileListView(LoginRequiredMixin, View):
    template_name = 'avrcompiler/files.html'

    def get(self, request, *args, **kwargs):
        # get files for user
        context = {}
        programs_list = AssemblyProgram.objects.filter(user=request.user)
        context = programs_list
        # render on page
        return render(request, self.template_name, {'files': context,})

class FileView(LoginRequiredMixin, View):
    template_name = 'avrcompiler/save_file.html'

    def get(self, request, *args, **kwargs):
        # get file and pass to 'compiler' to render
        context = {'id': '', 'code': '', 'name':'',}
        program = AssemblyProgram.objects.get(id=kwargs['pk'])
        if program:
            context['id'] = kwargs['pk']
            context['code'] = program.getCode()
            context['name'] = program.getName()
            request.session['program'] = context
        # redirect to page
        return  HttpResponseRedirect(reverse('compiler', args=(),kwargs={}));

    def post(self, request, *args, **kwargs):
        # TODO:  Fix this!!
        # get fields
        data = {}
        code = request.POST.get('code')
        name = request.POST.get('progname')
        id = request.POST.get('progid')

        if id is None:
            # create new object
            program = AssemblyProgram.create(name=name,code=code,user=request.user)
        else:
            program = AssemblyProgram.objects.get(name=name,user=request.user).save()
        # render, successfully updated
        request.session['id'] = program.getId()
        request.session['name'] = name
        request.session['code'] = code
        return HttpResponseRedirect("/")


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
from forms import RegisterForm


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

class RegisterView(View):
    #form_class = RegisterForm
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'registration/register.html'

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super(RegisterView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        context = {'form': form}
        return render_to_response(self.template_name, RequestContext(request, context))

    def post(self, request, *args, **kwargs):
        """
        Source: http://www.djangobook.com/en/2.0/chapter14.html
        """
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/login")
        else:
            return render(request, self.template_name, {'form': form,})