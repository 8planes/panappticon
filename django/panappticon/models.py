from django.db import models

class FileUpload(models.Model):
    date_received = models.DateTimeField(auto_now_add=True)
    file_id = models.CharField(max_length=255, unique=True)
    contents = models.CharField(max_length=16535)

class Application(models.Model):
    name = models.CharField(max_length=255, blank=True)
    app_id = models.CharField(max_length=255, unique=True)

class ApplicationUser(models.Model):
    name = models.CharField(max_length=255, blank=True)
    iphone_udid = models.CharField(max_length=255, blank=True)
    web_user = models.CharField(max_length=255, blank=True)

class Session(models.Model):
    user = models.ForeignKey(ApplicationUser, null=False)
    file_upload = models.ForeignKey(FileUpload, null=True)
    application = models.ForeignKey(Application, null=False)
    session_id = models.CharField(max_length=255, unique=True)
    start_time = models.DateTimeField(null=False)

class Screenshot(models.Model):
    date_received = models.DateTimeField(auto_now_add=True)
    key = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to="panappticon_screenshots", 
                              null=False)

class Tag(models.Model):
    file_upload = models.ForeignKey(FileUpload, null=True)
    line_number = models.IntegerField()
    session = models.ForeignKey(Session, null=False)
    tag = models.CharField(max_length=1023)
    date = models.DateTimeField(null=False)
    screenshot_key = models.CharField(max_length=255, blank=True)
    screenshot = models.ForeignKey(Screenshot, null=True)

