from panappticon import models
from dateutil import parser
from pytz import timezone
import os
import urllib
from django.utils import simplejson

def handle_screenshot_upload(file):
    name, ext = os.path.splitext(file.name)
    screenshot, created = models.Screenshot.objects.get_or_create(
        key=name,
        defaults={'image': file})
    tags = list(models.Tag.objects.filter(screenshot_key__exact=name))
    if len(tags) > 0:
        tag = tags[0]
        tag.screenshot = screenshot
        tag.save()

def _parse_date(date_string):
    eastern = timezone('US/Eastern')
    return parser.parse(date_string)\
        .astimezone(eastern).replace(tzinfo=None)
    

def handle_session_upload(file):
    contents = file.read()

    lines = contents.split('\n')

    # to accomodate max length in db
    contents = contents[:16534]

    file_id = lines[0]
    file_upload, created = models.FileUpload.objects.get_or_create(
        file_id=file_id,
        defaults={'contents': contents})

    if not created:
        return

    app_id = lines[1].strip()
    device_udid = lines[2].strip()
    session_id = lines[3].strip()
    session_start_time = _parse_date(lines[4].strip())
    coords = _coords(lines[5].strip())

    app, created = models.Application.objects.get_or_create(
        app_id = app_id)

    app_user, created = models.ApplicationUser.objects.get_or_create(
        iphone_udid=device_udid)

    session = models.Session(
        user=app_user,
        file_upload=file_upload,
        application=app,
        session_id=session_id,
        start_time=session_start_time,
        latitude=coords[0],
        longitude=coords[1],
        address=_address(coords[0], coords[1]))
    session.save()

    line_no = 7
    num_lines = len(lines)
    while line_no < num_lines - 2:
        _create_tag(line_no, lines, session, file_upload)
        line_no += 5

    session = models.Session.objects.get(pk=session.pk)
    session.update_stats()
    session.save()
    app_user.update_stats()
    app_user.save()

def _create_tag(line_no, lines, session, file_upload):
    tag_string = lines[line_no]
    screenshot_key = lines[line_no + 1]
    date = _parse_date(lines[line_no + 2])
    coords = _coords(lines[line_no + 3].strip())
    tag = models.Tag(
        file_upload=file_upload,
        line_number=line_no,
        session=session,
        tag=tag_string,
        date=date,
        screenshot_key=screenshot_key,
        latitude=coords[0],
        longitude=coords[1])
    if len(screenshot_key) > 0 and \
            models.Screenshot.objects.filter(key=screenshot_key).count() > 0:
        tag.screenshot = models.Screenshot.objects.get(key=screenshot_key)
    tag.save()

def _coords(coord_string):
    if coord_string:
        return [float(num) for num in coord_string.split(',')]
    else:
        return [None, None]

def _address(lat, lng):
    if lat is not None and lng is not None:
        try:
            f = urllib.urlopen(
                'http://maps.googleapis.com/maps/api/geocode/json?latlng={0},{1}&sensor=false'.format(
                    lat, lng))
            s = f.read()
            f.close()
            response = simplejson.loads(s)
            return response['results'][0]['formatted_address']
        except:
            return ''
    else:
        return ''
