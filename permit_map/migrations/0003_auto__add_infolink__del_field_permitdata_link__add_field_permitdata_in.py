# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'InfoLink'
        db.create_table(u'permit_map_infolink', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('link', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True)),
            ('image', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal(u'permit_map', ['InfoLink'])

        # Deleting field 'PermitData.link'
        db.delete_column(u'permit_map_permitdata', 'link')

        # Adding field 'PermitData.info_link'
        db.add_column(u'permit_map_permitdata', 'info_link',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['permit_map.InfoLink'], null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'InfoLink'
        db.delete_table(u'permit_map_infolink')

        # Adding field 'PermitData.link'
        db.add_column(u'permit_map_permitdata', 'link',
                      self.gf('django.db.models.fields.CharField')(max_length=1024, null=True),
                      keep_default=False)

        # Deleting field 'PermitData.info_link'
        db.delete_column(u'permit_map_permitdata', 'info_link_id')


    models = {
        u'permit_map.infolink': {
            'Meta': {'object_name': 'InfoLink'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True'})
        },
        u'permit_map.permitarea': {
            'Meta': {'object_name': 'PermitArea'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'first_seen': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_seen': ('django.db.models.fields.DateField', [], {}),
            'region': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {}),
            'township': ('django.db.models.fields.CharField', [], {'max_length': '4'})
        },
        u'permit_map.permitdata': {
            'Meta': {'object_name': 'PermitData'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info_link': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['permit_map.InfoLink']", 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'data'", 'to': u"orm['permit_map.PermitArea']"}),
            'proj_id': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True'}),
            'saved_on': ('django.db.models.fields.DateField', [], {}),
            'search_index': ('djorm_pgfulltext.fields.VectorField', [], {'default': "''", 'null': 'True', 'db_index': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True'})
        }
    }

    complete_apps = ['permit_map']