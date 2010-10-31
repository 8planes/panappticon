import logging
import os
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from panappticon import upload_handler, models
from panappticon import forms
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from decorators import render_to
from django.contrib.auth.decorators import login_required


@login_required
@render_to('panappticon/index.html')
def index(request):
    users = models.ApplicationUser.objects.all().order_by('id')
    return {'users': _paginated_records(request, users)}

@login_required
@render_to('panappticon/user.html')
def user(request, id):
    user = models.ApplicationUser.objects.get(id=id)
    return {'user': user, 'sessions': user.session_set.all() }

@login_required
def user_edit(request, id):
    user = models.ApplicationUser.objects.get(id=id)
    if request.method == 'POST':
        form = forms.EditApplicationUserForm(
            request.POST,
            instance=user)
        form.save()
        return redirect('panappticon:user', id)
    else:
        form = forms.EditApplicationUserForm(instance=user)
        context = { 'form': form, 'user': user }
        return render_to_response(
            'panappticon/user_edit.html', context,
            context_instance=RequestContext(request))    


@login_required
@render_to('panappticon/session.html')
def session(request, id):
    session = models.Session.objects.get(id=id)
    return { 'session': session, 'tags': session.tag_set.all() }

def iphone_upload(request):
    try:
        file = request.FILES['file']
        name, ext = os.path.splitext(file.name)
        print(ext)
        if ext == ".txt":
            upload_handler.handle_session_upload(file)
        else:
            upload_handler.handle_screenshot_upload(file)
    except Exception as inst:
        print type(inst)
        print inst
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

def _paginated_records(request, record_list):
    paginator = Paginator(record_list, 25)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        return paginator.page(page)
    except (EmptyPage, InvalidPage):
        return paginator.page(paginator.num_pages)
