# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'HelloSignRequest.unclaimed_draft_guid'
        db.add_column(u'hello_sign_hellosignrequest', 'unclaimed_draft_guid',
                      self.gf('django.db.models.fields.CharField')(db_index=True, max_length=128, null=True, blank=True),
                      keep_default=False)


        # Changing field 'HelloSignRequest.signature_request_id'
        db.alter_column(u'hello_sign_hellosignrequest', 'signature_request_id', self.gf('django.db.models.fields.CharField')(max_length=128, null=True))

    def backwards(self, orm):
        # Deleting field 'HelloSignRequest.unclaimed_draft_guid'
        db.delete_column(u'hello_sign_hellosignrequest', 'unclaimed_draft_guid')


        # User chose to not deal with backwards NULL issues for 'HelloSignRequest.signature_request_id'
        raise RuntimeError("Cannot reverse this migration. 'HelloSignRequest.signature_request_id' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'HelloSignRequest.signature_request_id'
        db.alter_column(u'hello_sign_hellosignrequest', 'signature_request_id', self.gf('django.db.models.fields.CharField')(max_length=128))

    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'hello_sign.hellosignlog': {
            'Meta': {'ordering': "['-id']", 'object_name': 'HelloSignLog'},
            'data': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'dateof': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'event_type': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'request': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hello_sign.HelloSignRequest']"})
        },
        u'hello_sign.hellosignrequest': {
            'Meta': {'ordering': "['-dateof']", 'object_name': 'HelloSignRequest'},
            'content_object_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'data': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'dateof': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'signature_request_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'unclaimed_draft_guid': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '128', 'null': 'True', 'blank': 'True'})
        },
        u'hello_sign.hellosignsigningurl': {
            'Meta': {'object_name': 'HelloSignSigningUrl'},
            'data': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'dateof': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'expires_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_index': 'True'}),
            'has_been_viewed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'request': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hello_sign.HelloSignRequest']"}),
            'signature_id': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'})
        }
    }

    complete_apps = ['hello_sign']