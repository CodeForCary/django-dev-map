# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Permit.description'
        db.add_column(u'permit_map_permit', 'description',
                      self.gf('django.db.models.fields.TextField')(null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Permit.description'
        db.delete_column(u'permit_map_permit', 'description')


    models = {
        'permit_map.permit': {
            'Meta': {'object_name': 'Permit'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'region': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True'}),
            'search_index': ('djorm_pgfulltext.fields.VectorField', [], {'default': "''", 'null': 'True', 'db_index': 'True'})
        }
    }

    complete_apps = ['permit_map']