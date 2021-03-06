# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    depends_on = (
        ("storybase_asset", "0001_initial.py"),
    )

    def forwards(self, orm):
        
        # Adding model 'StoryTranslation'
        db.create_table('storybase_story_storytranslation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('translation_id', self.gf('uuidfield.fields.UUIDField')(unique=True, max_length=32, blank=True)),
            ('language', self.gf('django.db.models.fields.CharField')(default='en', max_length=15)),
            ('story', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['storybase_story.Story'])),
            ('title', self.gf('storybase.fields.ShortTextField')()),
            ('summary', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
        ))
        db.send_create_signal('storybase_story', ['StoryTranslation'])

        # Adding unique constraint on 'StoryTranslation', fields ['story', 'language']
        db.create_unique('storybase_story_storytranslation', ['story_id', 'language'])

        # Adding model 'Story'
        db.create_table('storybase_story_story', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_edited', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default=u'draft', max_length=10)),
            ('published', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('license', self.gf('django.db.models.fields.CharField')(default='CC BY-NC-SA', max_length=25)),
            ('story_id', self.gf('uuidfield.fields.UUIDField')(unique=True, max_length=32, blank=True)),
            ('byline', self.gf('django.db.models.fields.TextField')()),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='stories', null=True, to=orm['auth.User'])),
        ))
        db.send_create_signal('storybase_story', ['Story'])

        # Adding M2M table for field assets on 'Story'
        db.create_table('storybase_story_story_assets', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('story', models.ForeignKey(orm['storybase_story.story'], null=False)),
            ('asset', models.ForeignKey(orm['storybase_asset.asset'], null=False))
        ))
        db.create_unique('storybase_story_story_assets', ['story_id', 'asset_id'])

        # Adding M2M table for field organizations on 'Story'
        db.create_table('storybase_story_story_organizations', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('story', models.ForeignKey(orm['storybase_story.story'], null=False)),
            ('organization', models.ForeignKey(orm['storybase_user.organization'], null=False))
        ))
        db.create_unique('storybase_story_story_organizations', ['story_id', 'organization_id'])

        # Adding M2M table for field projects on 'Story'
        db.create_table('storybase_story_story_projects', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('story', models.ForeignKey(orm['storybase_story.story'], null=False)),
            ('project', models.ForeignKey(orm['storybase_user.project'], null=False))
        ))
        db.create_unique('storybase_story_story_projects', ['story_id', 'project_id'])

        # Adding model 'Section'
        db.create_table('storybase_story_section', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('section_id', self.gf('uuidfield.fields.UUIDField')(unique=True, max_length=32, blank=True)),
            ('story', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sections', to=orm['storybase_story.Story'])),
            ('root', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('storybase_story', ['Section'])

        # Adding model 'SectionTranslation'
        db.create_table('storybase_story_sectiontranslation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('translation_id', self.gf('uuidfield.fields.UUIDField')(unique=True, max_length=32, blank=True)),
            ('language', self.gf('django.db.models.fields.CharField')(default='en', max_length=15)),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['storybase_story.Section'])),
            ('title', self.gf('storybase.fields.ShortTextField')()),
        ))
        db.send_create_signal('storybase_story', ['SectionTranslation'])

        # Adding unique constraint on 'SectionTranslation', fields ['section', 'language']
        db.create_unique('storybase_story_sectiontranslation', ['section_id', 'language'])

        # Adding model 'SectionRelation'
        db.create_table('storybase_story_sectionrelation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='section_child', to=orm['storybase_story.Section'])),
            ('child', self.gf('django.db.models.fields.related.ForeignKey')(related_name='section_parent', to=orm['storybase_story.Section'])),
            ('weight', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('storybase_story', ['SectionRelation'])

        # Adding model 'SectionAsset'
        db.create_table('storybase_story_sectionasset', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['storybase_story.Section'])),
            ('asset', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['storybase_asset.Asset'])),
            ('weight', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('storybase_story', ['SectionAsset'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'SectionTranslation', fields ['section', 'language']
        db.delete_unique('storybase_story_sectiontranslation', ['section_id', 'language'])

        # Removing unique constraint on 'StoryTranslation', fields ['story', 'language']
        db.delete_unique('storybase_story_storytranslation', ['story_id', 'language'])

        # Deleting model 'StoryTranslation'
        db.delete_table('storybase_story_storytranslation')

        # Deleting model 'Story'
        db.delete_table('storybase_story_story')

        # Removing M2M table for field assets on 'Story'
        db.delete_table('storybase_story_story_assets')

        # Removing M2M table for field organizations on 'Story'
        db.delete_table('storybase_story_story_organizations')

        # Removing M2M table for field projects on 'Story'
        db.delete_table('storybase_story_story_projects')

        # Deleting model 'Section'
        db.delete_table('storybase_story_section')

        # Deleting model 'SectionTranslation'
        db.delete_table('storybase_story_sectiontranslation')

        # Deleting model 'SectionRelation'
        db.delete_table('storybase_story_sectionrelation')

        # Deleting model 'SectionAsset'
        db.delete_table('storybase_story_sectionasset')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'storybase_asset.asset': {
            'Meta': {'object_name': 'Asset'},
            'asset_created': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'asset_id': ('uuidfield.fields.UUIDField', [], {'unique': 'True', 'max_length': '32', 'blank': 'True'}),
            'attribution': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'datasets': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'assets'", 'blank': 'True', 'to': "orm['storybase_asset.DataSet']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_edited': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'license': ('django.db.models.fields.CharField', [], {'default': "'CC BY-NC-SA'", 'max_length': '25'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'assets'", 'null': 'True', 'to': "orm['auth.User']"}),
            'published': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'section_specific': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'source_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "u'draft'", 'max_length': '10'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'storybase_asset.dataset': {
            'Meta': {'object_name': 'DataSet'},
            'attribution': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dataset_created': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'dataset_id': ('uuidfield.fields.UUIDField', [], {'unique': 'True', 'max_length': '32', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_edited': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'datasets'", 'null': 'True', 'to': "orm['auth.User']"}),
            'published': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "u'draft'", 'max_length': '10'})
        },
        'storybase_story.section': {
            'Meta': {'object_name': 'Section'},
            'assets': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'sections'", 'blank': 'True', 'through': "orm['storybase_story.SectionAsset']", 'to': "orm['storybase_asset.Asset']"}),
            'children': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['storybase_story.Section']", 'null': 'True', 'through': "orm['storybase_story.SectionRelation']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'root': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'section_id': ('uuidfield.fields.UUIDField', [], {'unique': 'True', 'max_length': '32', 'blank': 'True'}),
            'story': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sections'", 'to': "orm['storybase_story.Story']"})
        },
        'storybase_story.sectionasset': {
            'Meta': {'object_name': 'SectionAsset'},
            'asset': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['storybase_asset.Asset']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['storybase_story.Section']"}),
            'weight': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'storybase_story.sectionrelation': {
            'Meta': {'object_name': 'SectionRelation'},
            'child': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'section_parent'", 'to': "orm['storybase_story.Section']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'section_child'", 'to': "orm['storybase_story.Section']"}),
            'weight': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'storybase_story.sectiontranslation': {
            'Meta': {'unique_together': "(('section', 'language'),)", 'object_name': 'SectionTranslation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '15'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['storybase_story.Section']"}),
            'title': ('storybase.fields.ShortTextField', [], {}),
            'translation_id': ('uuidfield.fields.UUIDField', [], {'unique': 'True', 'max_length': '32', 'blank': 'True'})
        },
        'storybase_story.story': {
            'Meta': {'object_name': 'Story'},
            'assets': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'stories'", 'blank': 'True', 'to': "orm['storybase_asset.Asset']"}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'stories'", 'null': 'True', 'to': "orm['auth.User']"}),
            'byline': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_edited': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'license': ('django.db.models.fields.CharField', [], {'default': "'CC BY-NC-SA'", 'max_length': '25'}),
            'organizations': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'stories'", 'blank': 'True', 'to': "orm['storybase_user.Organization']"}),
            'projects': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'stories'", 'blank': 'True', 'to': "orm['storybase_user.Project']"}),
            'published': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "u'draft'", 'max_length': '10'}),
            'story_id': ('uuidfield.fields.UUIDField', [], {'unique': 'True', 'max_length': '32', 'blank': 'True'})
        },
        'storybase_story.storytranslation': {
            'Meta': {'unique_together': "(('story', 'language'),)", 'object_name': 'StoryTranslation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '15'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'story': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['storybase_story.Story']"}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('storybase.fields.ShortTextField', [], {}),
            'translation_id': ('uuidfield.fields.UUIDField', [], {'unique': 'True', 'max_length': '32', 'blank': 'True'})
        },
        'storybase_user.organization': {
            'Meta': {'object_name': 'Organization'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'curated_stories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'curated_in_organizations'", 'blank': 'True', 'through': "orm['storybase_user.OrganizationStory']", 'to': "orm['storybase_story.Story']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_edited': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'organizations'", 'blank': 'True', 'to': "orm['auth.User']"}),
            'organization_id': ('uuidfield.fields.UUIDField', [], {'unique': 'True', 'max_length': '32', 'blank': 'True'}),
            'website_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'storybase_user.organizationstory': {
            'Meta': {'object_name': 'OrganizationStory'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['storybase_user.Organization']"}),
            'story': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['storybase_story.Story']"}),
            'weight': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'storybase_user.project': {
            'Meta': {'object_name': 'Project'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'curated_stories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'curated_in_projects'", 'blank': 'True', 'through': "orm['storybase_user.ProjectStory']", 'to': "orm['storybase_story.Story']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_edited': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'projects'", 'blank': 'True', 'to': "orm['auth.User']"}),
            'organizations': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'projects'", 'blank': 'True', 'to': "orm['storybase_user.Organization']"}),
            'project_id': ('uuidfield.fields.UUIDField', [], {'unique': 'True', 'max_length': '32', 'blank': 'True'}),
            'website_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'storybase_user.projectstory': {
            'Meta': {'object_name': 'ProjectStory'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['storybase_user.Project']"}),
            'story': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['storybase_story.Story']"}),
            'weight': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['storybase_story']
