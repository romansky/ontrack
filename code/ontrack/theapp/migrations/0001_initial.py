# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tag'
        db.create_table('theapp_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('theapp', ['Tag'])

        # Adding model 'User'
        db.create_table('theapp_user', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('user_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('join_time', self.gf('django.db.models.fields.BigIntegerField')()),
            ('weight', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('theapp', ['User'])

        # Adding model 'Link'
        db.create_table('theapp_link', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('link_type', self.gf('django.db.models.fields.IntegerField')()),
            ('notes', self.gf('django.db.models.fields.TextField')()),
            ('date_added', self.gf('django.db.models.fields.BigIntegerField')()),
            ('who_added', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['theapp.User'])),
            ('thumb', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True)),
        ))
        db.send_create_signal('theapp', ['Link'])

        # Adding model 'Track'
        db.create_table('theapp_track', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('level', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('created_time', self.gf('django.db.models.fields.BigIntegerField')()),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['theapp.User'])),
            ('unique_url', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('theapp', ['Track'])

        # Adding M2M table for field links on 'Track'
        db.create_table('theapp_track_links', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('track', models.ForeignKey(orm['theapp.track'], null=False)),
            ('link', models.ForeignKey(orm['theapp.link'], null=False))
        ))
        db.create_unique('theapp_track_links', ['track_id', 'link_id'])

        # Adding M2M table for field tags on 'Track'
        db.create_table('theapp_track_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('track', models.ForeignKey(orm['theapp.track'], null=False)),
            ('tag', models.ForeignKey(orm['theapp.tag'], null=False))
        ))
        db.create_unique('theapp_track_tags', ['track_id', 'tag_id'])

        # Adding model 'Comment'
        db.create_table('theapp_comment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('vote_type', self.gf('django.db.models.fields.IntegerField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['theapp.User'])),
            ('track', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['theapp.Track'])),
            ('when', self.gf('django.db.models.fields.BigIntegerField')()),
        ))
        db.send_create_signal('theapp', ['Comment'])

        # Adding model 'ShareLog'
        db.create_table('theapp_sharelog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('where_to', self.gf('django.db.models.fields.IntegerField')()),
            ('when', self.gf('django.db.models.fields.BigIntegerField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['theapp.User'])),
            ('track', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['theapp.Track'])),
        ))
        db.send_create_signal('theapp', ['ShareLog'])


    def backwards(self, orm):
        # Deleting model 'Tag'
        db.delete_table('theapp_tag')

        # Deleting model 'User'
        db.delete_table('theapp_user')

        # Deleting model 'Link'
        db.delete_table('theapp_link')

        # Deleting model 'Track'
        db.delete_table('theapp_track')

        # Removing M2M table for field links on 'Track'
        db.delete_table('theapp_track_links')

        # Removing M2M table for field tags on 'Track'
        db.delete_table('theapp_track_tags')

        # Deleting model 'Comment'
        db.delete_table('theapp_comment')

        # Deleting model 'ShareLog'
        db.delete_table('theapp_sharelog')


    models = {
        'theapp.comment': {
            'Meta': {'object_name': 'Comment'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'track': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['theapp.Track']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['theapp.User']"}),
            'vote_type': ('django.db.models.fields.IntegerField', [], {}),
            'when': ('django.db.models.fields.BigIntegerField', [], {})
        },
        'theapp.link': {
            'Meta': {'object_name': 'Link'},
            'date_added': ('django.db.models.fields.BigIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link_type': ('django.db.models.fields.IntegerField', [], {}),
            'notes': ('django.db.models.fields.TextField', [], {}),
            'thumb': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'who_added': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['theapp.User']"})
        },
        'theapp.sharelog': {
            'Meta': {'object_name': 'ShareLog'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'track': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['theapp.Track']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['theapp.User']"}),
            'when': ('django.db.models.fields.BigIntegerField', [], {}),
            'where_to': ('django.db.models.fields.IntegerField', [], {})
        },
        'theapp.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'theapp.track': {
            'Meta': {'object_name': 'Track'},
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['theapp.User']"}),
            'created_time': ('django.db.models.fields.BigIntegerField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'links': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['theapp.Link']", 'symmetrical': 'False'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['theapp.Tag']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'unique_url': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'theapp.user': {
            'Meta': {'object_name': 'User'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'join_time': ('django.db.models.fields.BigIntegerField', [], {}),
            'user_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'weight': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['theapp']