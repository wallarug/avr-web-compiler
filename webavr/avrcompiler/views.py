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