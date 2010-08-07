from django.db import models

class FileUpload(models.Model):
    date_received = models.DateTimeField(auto_now_add=True)
    file_id = models.CharField(max_length=255, unique=True)
    contents = models.CharField(max_length=16535)

class Application(models.Model):
    name = models.CharField(max_length=255, blank=True)
    app_id = models.CharField(max_length=255, unique=True)

class Session(models.Model):
    file_upload = models.ForeignKey(FileUpload, null=False)
    application = models.ForeignKey(Application, null=False)
    session_id = models.CharField(max_length=255, unique=True)
    start_time = models.DateTimeField(null=False)

class Tag(models.Model):
    file_upload = models.ForeignKey(FileUpload, null=False)
    line_number = models.IntegerField
    session = models.ForeignKey(Session, null=False)
    tag = models.CharField(max_length=1023)
    date = models.DateTimeField(null=False)
    screenshot_key = models.CharField(max_length=255, blank=True)
    screenshot = models.ImageField(upload_to="panappticon_screenshots", null=True)

class ScreenshotOrphan(models.Model):
    date_received = models.DateTimeField(auto_now_add=True)
    screenshot_key = models.CharField(max_length=255, unique=True)
    screenshot = models.ImageField(upload_to="panappticon_screenshots", null=False)