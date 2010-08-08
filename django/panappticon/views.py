import logging
import os
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from panappticon import upload_handler, models

def index(request):
    return render_to_response('index.html', {}, RequestContext(request))

def iphone_upload(request):
    file = request.FILES['file']
    name, ext = os.path.splitext(file.name)
    if ext == ".txt":
        upload_handler.handle_session_upload(file)
    else:
        upload_handler.handle_screenshot_upload(file)
    return HttpResponse("yes!", mimetype="text/plain")

def jsonp_tag(request):
    _web_tag(request.GET)
    return HttpReponse(
        "{0}('ok!');".format(request.GET['callback']),
        mimetype="text/javascript")

def xhr_tag(request):
    _web_tag(request.POST)
    return HttpResponse("ok!", mimetype="text/plain")

def _web_tag(query_dict):
    # do this in future
    pass
