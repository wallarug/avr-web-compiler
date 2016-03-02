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

from django.contrib.auth.mixins import LoginRequiredMixin
from .models import AssemblyProgram


class CompileView(LoginRequiredMixin,View):
    template_name = 'avrcompiler/main.html'

    def get(self, request, *args, **kwargs):
        data = {}
        try:
            errors = request.session['errors']
            data['errormessage'] = errors
            del request.session['errors']
        except KeyError:
            pass
        try:
            message = request.session['message']
            data['message'] = message
            del request.session['message']
        except KeyError:
            pass
        try:
            success = request.session['successmessage']
            data['successmessage'] = success
            del request.session['successmessage']
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
            data['id'] = 'None'
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
        if "# ERROR: " in message:
            data['errormessage'] = "Something went wrong, check bottom for details."
        else:
            data['successmessage'] = "Program successfully compiled and uploaded!"
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
        print id

        if id == 'None':
            # create new object
            print "create"
            program = AssemblyProgram.objects.create(code=code,name=name,user=request.user)
        else:
            print "save"
            program = AssemblyProgram.objects.get(id=id)
            if program.getName() == name:
                # everything checks out, save updated version of code.
                program.save(code=code)
            else:
                # create instead because name has changed
                program = AssemblyProgram.objects.create(code=code,name=name,user=request.user)

        # render, successfully updated
        if program:
            context = {}
            context['id'] = program.getId()
            context['code'] = program.getCode()
            context['name'] = program.getName()
            request.session['program'] = context
            request.session['successmessage'] = "File Successfully Saved!"
        # redirect to page
        return  HttpResponseRedirect(reverse('compiler', args=(),kwargs={}));
        #return HttpResponseRedirect("/")
