import logging
import os
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from panappticon import session_file_handler, models

def index(request):
    if request.method == "POST":
        return _handle_upload(request)
    else:
        return render_to_response('index.html', {}, RequestContext(request))

def _handle_upload(request):
    file = request.FILES['file']
    name, ext = os.path.splitext(file.name)
    if ext == ".txt":
        session_file_handler.handle_upload(file)
    else:
        _handle_screenshot_upload(file)
    return HttpResponse("yes!", mimetype="text/plain")

def _handle_screenshot_upload(file):
    name, ext = os.path.splitext(file.name)
    screenshot, created = models.Screenshot.get_or_create(
        key=name,
        defaults={'image': file})
    tags = list(models.Tag.objects.filter(screenshot_key__exact=name))
    if len(tags) > 0:
        tag = tags[0]
        tag.screenshot = screenshot
        tag.save()
