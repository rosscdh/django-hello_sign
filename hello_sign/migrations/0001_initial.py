# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'HelloSignRequest'
        db.create_table(u'hello_sign_hellosignrequest', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_object_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('signature_request_id', self.gf('django.db.models.fields.CharField')(max_length=128, db_index=True)),
            ('dateof', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('data', self.gf('jsonfield.fields.JSONField')(default={})),
        ))
        db.send_create_signal(u'hello_sign', ['HelloSignRequest'])

        # Adding model 'HelloSignLog'
        db.create_table(u'hello_sign_hellosignlog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('request', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hello_sign.HelloSignRequest'])),
            ('event_type', self.gf('django.db.models.fields.CharField')(max_length=32, db_index=True)),
            ('dateof', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('data', self.gf('jsonfield.fields.JSONField')(default={})),
        ))
        db.send_create_signal(u'hello_sign', ['HelloSignLog'])

        # Adding model 'HelloSignSigningUrl'
        db.create_table(u'hello_sign_hellosignsigningurl', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('request', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hello_sign.HelloSignRequest'])),
            ('signature_id', self.gf('django.db.models.fields.CharField')(max_length=128, db_index=True)),
            ('has_been_viewed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('expires_at', self.gf('django.db.models.fields.DateTimeField')(null=True, db_index=True)),
            ('dateof', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('data', self.gf('jsonfield.fields.JSONField')(default={})),
        ))
        db.send_create_signal(u'hello_sign', ['HelloSignSigningUrl'])


    def backwards(self, orm):
        # Deleting model 'HelloSignRequest'
        db.delete_table(u'hello_sign_hellosignrequest')

        # Deleting model 'HelloSignLog'
        db.delete_table(u'hello_sign_hellosignlog')

        # Deleting model 'HelloSignSigningUrl'
        db.delete_table(u'hello_sign_hellosignsigningurl')


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
            'signature_request_id': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'})
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