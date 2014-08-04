# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Permit'
        db.create_table(u'permit_map_permit', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('region', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(null=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True)),
            ('proj_id', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True)),
            ('link', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True)),
            ('search_index', self.gf('djorm_pgfulltext.fields.VectorField')(default='', null=True, db_index=True)),
        ))
        db.send_create_signal(u'permit_map', ['Permit'])


    def backwards(self, orm):
        # Deleting model 'Permit'
        db.delete_table(u'permit_map_permit')


    models = {
        u'permit_map.permit': {
            'Meta': {'object_name': 'Permit'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True'}),
            'proj_id': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True'}),
            'region': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True'}),
            'search_index': ('djorm_pgfulltext.fields.VectorField', [], {'default': "''", 'null': 'True', 'db_index': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True'})
        }
    }

    complete_apps = ['permit_map']