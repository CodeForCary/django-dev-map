# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Permit.name'
        db.add_column(u'permit_map_permit', 'name',
                      self.gf('django.db.models.fields.CharField')(max_length=1024, null=True),
                      keep_default=False)

        # Adding field 'Permit.comment'
        db.add_column(u'permit_map_permit', 'comment',
                      self.gf('django.db.models.fields.CharField')(max_length=1024, null=True),
                      keep_default=False)

        # Adding field 'Permit.proj_id'
        db.add_column(u'permit_map_permit', 'proj_id',
                      self.gf('django.db.models.fields.CharField')(max_length=1024, null=True),
                      keep_default=False)

        # Adding field 'Permit.link'
        db.add_column(u'permit_map_permit', 'link',
                      self.gf('django.db.models.fields.CharField')(max_length=1024, null=True),
                      keep_default=False)

        # Adding field 'Permit.status'
        db.add_column(u'permit_map_permit', 'status',
                      self.gf('django.db.models.fields.CharField')(max_length=1024, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Permit.name'
        db.delete_column(u'permit_map_permit', 'name')

        # Deleting field 'Permit.comment'
        db.delete_column(u'permit_map_permit', 'comment')

        # Deleting field 'Permit.proj_id'
        db.delete_column(u'permit_map_permit', 'proj_id')

        # Deleting field 'Permit.link'
        db.delete_column(u'permit_map_permit', 'link')

        # Deleting field 'Permit.status'
        db.delete_column(u'permit_map_permit', 'status')


    models = {
        u'permit_map.permit': {
            'Meta': {'object_name': 'Permit'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
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