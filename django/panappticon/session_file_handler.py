from panappticon import models
from dateutil import parser

def handle_upload(file):
    with open(file, "r") as f:
        contents = f.read()

    lines = content.split('\n')
    
    file_id = lines[0]
    file_upload, created = models.FileUpload.get_or_create(
        file_id=file_id,
        defaults={'contents': contents})

    if not created:
        return

    app_id = lines[1].strip()
    session_id = lines[2].strip()
    session_start_time = parser.parse(lines[3].strip())

    app, created = models.Application.get_or_create(
        app_id = app_id)

    session = models.Session(
        file_upload = file_upload,
        application = application,
        session_id = session_id,
        start_time = session_start_time)
    session.save()

    line_no = 5
    num_lines = len(lines)
    while line_no < num_lines:
        _create_tag(line_no, lines, session, file_upload)
        line_no += 4

def _create_tag(line_no, lines, session, file_upload):
    tag_string = lines[line_no]
    screenshot_key = lines[line_no + 1]
    date = parser.parse(lines[line_no + 2])
    tag = models.Tag(
        file_upload = file_upload,
        line_number = line_no,
        session = session,
        tag = tag_string,
        date = date,
        screenshot_key = screenshot_key)
    if len(screenshot_key) > 0 and \
            models.Screenshot.objects.exists(key=screenshot_key):
        tag.screenshot = models.Screenshot.get(key=screenshot_key)
    tag.save()
