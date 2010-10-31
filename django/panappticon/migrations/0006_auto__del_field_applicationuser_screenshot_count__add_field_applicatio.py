# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'ApplicationUser.screenshot_count'
        db.delete_column('panappticon_applicationuser', 'screenshot_count')

        # Adding field 'ApplicationUser.tag_count'
        db.add_column('panappticon_applicationuser', 'tag_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0), keep_default=False)


    def backwards(self, orm):
        
        # Adding field 'ApplicationUser.screenshot_count'
        db.add_column('panappticon_applicationuser', 'screenshot_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0), keep_default=False)

        # Deleting field 'ApplicationUser.tag_count'
        db.delete_column('panappticon_applicationuser', 'tag_count')


    models = {
        'panappticon.application': {
            'Meta': {'object_name': 'Application'},
            'app_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'panappticon.applicationuser': {
            'Meta': {'object_name': 'ApplicationUser'},
            'first_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iphone_udid': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'last_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '4095', 'blank': 'True'}),
            'session_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'tag_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
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
            'minutes_in_session': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'session_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {}),
            'tag_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
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
