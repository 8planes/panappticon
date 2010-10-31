# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'FileUpload'
        db.create_table('panappticon_fileupload', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_received', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('file_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('contents', self.gf('django.db.models.fields.CharField')(max_length=16535)),
        ))
        db.send_create_signal('panappticon', ['FileUpload'])

        # Adding model 'Application'
        db.create_table('panappticon_application', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('app_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('panappticon', ['Application'])

        # Adding model 'ApplicationUser'
        db.create_table('panappticon_applicationuser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('iphone_udid', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('web_user', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal('panappticon', ['ApplicationUser'])

        # Adding model 'Session'
        db.create_table('panappticon_session', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['panappticon.ApplicationUser'])),
            ('file_upload', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['panappticon.FileUpload'], null=True)),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['panappticon.Application'])),
            ('session_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('panappticon', ['Session'])

        # Adding model 'Screenshot'
        db.create_table('panappticon_screenshot', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_received', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('panappticon', ['Screenshot'])

        # Adding model 'Tag'
        db.create_table('panappticon_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file_upload', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['panappticon.FileUpload'], null=True)),
            ('line_number', self.gf('django.db.models.fields.IntegerField')()),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['panappticon.Session'])),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=1023)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('screenshot_key', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('screenshot', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['panappticon.Screenshot'], null=True)),
        ))
        db.send_create_signal('panappticon', ['Tag'])


    def backwards(self, orm):
        
        # Deleting model 'FileUpload'
        db.delete_table('panappticon_fileupload')

        # Deleting model 'Application'
        db.delete_table('panappticon_application')

        # Deleting model 'ApplicationUser'
        db.delete_table('panappticon_applicationuser')

        # Deleting model 'Session'
        db.delete_table('panappticon_session')

        # Deleting model 'Screenshot'
        db.delete_table('panappticon_screenshot')

        # Deleting model 'Tag'
        db.delete_table('panappticon_tag')


    models = {
        'panappticon.application': {
            'Meta': {'object_name': 'Application'},
            'app_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'panappticon.applicationuser': {
            'Meta': {'object_name': 'ApplicationUser'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iphone_udid': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'web_user': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'panappticon.fileupload': {
            'Meta': {'object_name': 'FileUpload'},
            'contents': ('django.db.models.fields.CharField', [], {'max_length': '16535'}),
            'date_received': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'file_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'panappticon.screenshot': {
            'Meta': {'object_name': 'Screenshot'},
            'date_received': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'panappticon.session': {
            'Meta': {'object_name': 'Session'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['panappticon.Application']"}),
            'file_upload': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['panappticon.FileUpload']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'session_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['panappticon.ApplicationUser']"})
        },
        'panappticon.tag': {
            'Meta': {'object_name': 'Tag'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'file_upload': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['panappticon.FileUpload']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line_number': ('django.db.models.fields.IntegerField', [], {}),
            'screenshot': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['panappticon.Screenshot']", 'null': 'True'}),
            'screenshot_key': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['panappticon.Session']"}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '1023'})
        }
    }

    complete_apps = ['panappticon']
