from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField

class FileUpload(models.Model):
    date_received = models.DateTimeField(auto_now_add=True)
    file_id = models.CharField(max_length=255, unique=True)
    contents = models.CharField(max_length=16535)

class Application(models.Model):
    name = models.CharField(max_length=255, blank=True)
    app_id = models.CharField(max_length=255, unique=True)

class ApplicationUser(models.Model):
    name = models.CharField(max_length=255, blank=True)
    notes = models.TextField(max_length=4095, blank=True)
    iphone_udid = models.CharField(max_length=255, blank=True)
    web_user = models.CharField(max_length=255, blank=True)
    session_count = models.PositiveIntegerField(default=0)
    tag_count = models.PositiveIntegerField(default=0)
    first_date = models.DateTimeField(null=False, auto_now_add=True)
    last_date = models.DateTimeField(null=False, auto_now_add=True)

    @property
    def name_to_use(self):
        return self.name if self.name else iphone_udid

    def update_stats(self):
        all_sessions = self.session_set.all()
        self.session_count = len(all_sessions)
        self.tag_count = sum([s.tag_count for s in all_sessions])
        self.last_date = max([s.start_time for s in all_sessions])

class Session(models.Model):
    user = models.ForeignKey(ApplicationUser, null=False)
    file_upload = models.ForeignKey(FileUpload, null=True)
    application = models.ForeignKey(Application, null=False)
    session_id = models.CharField(max_length=255, unique=True)
    start_time = models.DateTimeField(null=False)
    tag_count = models.PositiveIntegerField(default=0)
    minutes_in_session = models.FloatField(default=0)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    address = models.CharField(max_length=511, blank=True)

    def update_stats(self):
        self.tag_count = self.tag_set.count()
        max_tag_date = max([t.date for t in self.tag_set.all()])
        timedelta = max_tag_date - self.start_time
        self.minutes_in_session = timedelta.seconds / 60.0

class Screenshot(models.Model):
    date_received = models.DateTimeField(auto_now_add=True)
    key = models.CharField(max_length=255, unique=True)
    image = models.ImageField(
        null=False,
        upload_to="panappticon_screenshots")

class Tag(models.Model):
    file_upload = models.ForeignKey(FileUpload, null=True)
    line_number = models.IntegerField()
    session = models.ForeignKey(Session, null=False)
    tag = models.CharField(max_length=1023)
    date = models.DateTimeField(null=False)
    screenshot_key = models.CharField(max_length=255, blank=True)
    screenshot = models.ForeignKey(Screenshot, null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

