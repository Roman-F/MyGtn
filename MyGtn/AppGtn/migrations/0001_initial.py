# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EntityNaturalPerson'
        db.create_table(u'AppGtn_entitynaturalperson', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('modifided_date', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('deleted_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=1000, blank=True)),
            ('surname', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('middlename', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('inn', self.gf('django.db.models.fields.PositiveIntegerField')(max_length=12, null=True, blank=True)),
            ('date_of_birth', self.gf('django.db.models.fields.DateField')()),
            ('place_of_birth', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('serial_dul', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('number_dul', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('date_issue_dul', self.gf('django.db.models.fields.DateField')()),
            ('groupfl', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'AppGtn', ['EntityNaturalPerson'])

        # Adding model 'EntityLegalPerson'
        db.create_table(u'AppGtn_entitylegalperson', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('modifided_date', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('deleted_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=1000, blank=True)),
        ))
        db.send_create_signal(u'AppGtn', ['EntityLegalPerson'])

        # Adding model 'EntityVehicle'
        db.create_table(u'AppGtn_entityvehicle', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('modifided_date', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('deleted_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=1000, blank=True)),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['AppGtn.VehicleBrand'])),
            ('color', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['AppGtn.VehicleColor'])),
            ('country_of_origin', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['AppGtn.Country'])),
            ('year_of_issue', self.gf('django.db.models.fields.PositiveSmallIntegerField')(max_length=4)),
            ('serial_psm', self.gf('django.db.models.fields.CharField')(max_length=2, blank=True)),
            ('number_psm', self.gf('django.db.models.fields.PositiveIntegerField')(max_length=6, blank=True)),
            ('date_of_issue_psm', self.gf('django.db.models.fields.DateField')(blank=True)),
            ('serial_number', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('engine_number', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('transmission_number', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('bridge_number', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
        ))
        db.send_create_signal(u'AppGtn', ['EntityVehicle'])

        # Adding model 'VehicleColor'
        db.create_table(u'AppGtn_vehiclecolor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('modifided_date', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('deleted_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=1000, blank=True)),
            ('color_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
        ))
        db.send_create_signal(u'AppGtn', ['VehicleColor'])

        # Adding model 'BrandEngine'
        db.create_table(u'AppGtn_brandengine', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('modifided_date', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('deleted_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=1000, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
        ))
        db.send_create_signal(u'AppGtn', ['BrandEngine'])

        # Adding model 'OrganizationIssue'
        db.create_table(u'AppGtn_organizationissue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('modifided_date', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('deleted_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=1000, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=300)),
            ('addr', self.gf('django.db.models.fields.CharField')(max_length=300)),
        ))
        db.send_create_signal(u'AppGtn', ['OrganizationIssue'])

        # Adding model 'Country'
        db.create_table(u'AppGtn_country', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('modifided_date', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('deleted_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=1000, blank=True)),
            ('full_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('short_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('code', self.gf('django.db.models.fields.IntegerField')(unique=True, max_length=3)),
            ('alpha_2', self.gf('django.db.models.fields.CharField')(unique=True, max_length=2)),
            ('alpha_3', self.gf('django.db.models.fields.CharField')(unique=True, max_length=3)),
        ))
        db.send_create_signal(u'AppGtn', ['Country'])

        # Adding model 'Manufacturer'
        db.create_table(u'AppGtn_manufacturer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('modifided_date', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('deleted_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=1000, blank=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['AppGtn.Country'])),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=300)),
            ('addr', self.gf('django.db.models.fields.CharField')(max_length=300)),
        ))
        db.send_create_signal(u'AppGtn', ['Manufacturer'])

        # Adding model 'KindVehicle'
        db.create_table(u'AppGtn_kindvehicle', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('modifided_date', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('deleted_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=1000, blank=True)),
            ('code', self.gf('django.db.models.fields.PositiveSmallIntegerField')(unique=True, max_length=3)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
        ))
        db.send_create_signal(u'AppGtn', ['KindVehicle'])

        # Adding model 'TypeProp'
        db.create_table(u'AppGtn_typeprop', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('modifided_date', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('deleted_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=1000, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
        ))
        db.send_create_signal(u'AppGtn', ['TypeProp'])

        # Adding model 'TypeAndGroupVehicle'
        db.create_table(u'AppGtn_typeandgroupvehicle', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('modifided_date', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('deleted_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=1000, blank=True)),
            ('parent_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('level', self.gf('django.db.models.fields.PositiveSmallIntegerField')(max_length=1)),
        ))
        db.send_create_signal(u'AppGtn', ['TypeAndGroupVehicle'])

        # Adding model 'VehicleEngine'
        db.create_table(u'AppGtn_vehicleengine', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('modifided_date', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('deleted_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=1000, blank=True)),
            ('brand_engine', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['AppGtn.BrandEngine'])),
            ('power_kwt', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('power_hp', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('working_voluem', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, max_length=10)),
            ('type_engine', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'AppGtn', ['VehicleEngine'])

        # Adding M2M table for field brand_vehicle on 'VehicleEngine'
        m2m_table_name = db.shorten_name(u'AppGtn_vehicleengine_brand_vehicle')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('vehicleengine', models.ForeignKey(orm[u'AppGtn.vehicleengine'], null=False)),
            ('vehiclebrand', models.ForeignKey(orm[u'AppGtn.vehiclebrand'], null=False))
        ))
        db.create_unique(m2m_table_name, ['vehicleengine_id', 'vehiclebrand_id'])

        # Adding model 'VehicleBrand'
        db.create_table(u'AppGtn_vehiclebrand', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('modifided_date', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('deleted_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=1000, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('type_brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['AppGtn.TypeAndGroupVehicle'])),
            ('manufacturer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['AppGtn.Manufacturer'])),
            ('brand_category', self.gf('django.db.models.fields.CharField')(max_length=11)),
            ('weight', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('max_speed', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('length', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('width', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('heigth', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('sertificate_number', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('sertificate_data', self.gf('django.db.models.fields.DateField')(blank=True)),
            ('sirtificate_issue', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['AppGtn.OrganizationIssue'], blank=True)),
            ('kind_vihicle', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['AppGtn.KindVehicle'])),
            ('type_prop', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['AppGtn.TypeProp'])),
        ))
        db.send_create_signal(u'AppGtn', ['VehicleBrand'])

        # Adding M2M table for field brand_engine on 'VehicleBrand'
        m2m_table_name = db.shorten_name(u'AppGtn_vehiclebrand_brand_engine')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('vehiclebrand', models.ForeignKey(orm[u'AppGtn.vehiclebrand'], null=False)),
            ('vehicleengine', models.ForeignKey(orm[u'AppGtn.vehicleengine'], null=False))
        ))
        db.create_unique(m2m_table_name, ['vehiclebrand_id', 'vehicleengine_id'])


    def backwards(self, orm):
        # Deleting model 'EntityNaturalPerson'
        db.delete_table(u'AppGtn_entitynaturalperson')

        # Deleting model 'EntityLegalPerson'
        db.delete_table(u'AppGtn_entitylegalperson')

        # Deleting model 'EntityVehicle'
        db.delete_table(u'AppGtn_entityvehicle')

        # Deleting model 'VehicleColor'
        db.delete_table(u'AppGtn_vehiclecolor')

        # Deleting model 'BrandEngine'
        db.delete_table(u'AppGtn_brandengine')

        # Deleting model 'OrganizationIssue'
        db.delete_table(u'AppGtn_organizationissue')

        # Deleting model 'Country'
        db.delete_table(u'AppGtn_country')

        # Deleting model 'Manufacturer'
        db.delete_table(u'AppGtn_manufacturer')

        # Deleting model 'KindVehicle'
        db.delete_table(u'AppGtn_kindvehicle')

        # Deleting model 'TypeProp'
        db.delete_table(u'AppGtn_typeprop')

        # Deleting model 'TypeAndGroupVehicle'
        db.delete_table(u'AppGtn_typeandgroupvehicle')

        # Deleting model 'VehicleEngine'
        db.delete_table(u'AppGtn_vehicleengine')

        # Removing M2M table for field brand_vehicle on 'VehicleEngine'
        db.delete_table(db.shorten_name(u'AppGtn_vehicleengine_brand_vehicle'))

        # Deleting model 'VehicleBrand'
        db.delete_table(u'AppGtn_vehiclebrand')

        # Removing M2M table for field brand_engine on 'VehicleBrand'
        db.delete_table(db.shorten_name(u'AppGtn_vehiclebrand_brand_engine'))


    models = {
        u'AppGtn.brandengine': {
            'Meta': {'object_name': 'BrandEngine'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'created_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifided_date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'AppGtn.country': {
            'Meta': {'object_name': 'Country'},
            'alpha_2': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2'}),
            'alpha_3': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '3'}),
            'code': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'max_length': '3'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'created_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'full_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifided_date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'AppGtn.entitylegalperson': {
            'Meta': {'object_name': 'EntityLegalPerson'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'created_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifided_date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'AppGtn.entitynaturalperson': {
            'Meta': {'object_name': 'EntityNaturalPerson'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'created_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_issue_dul': ('django.db.models.fields.DateField', [], {}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {}),
            'deleted_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'groupfl': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inn': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'middlename': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'modifided_date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'number_dul': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'place_of_birth': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'serial_dul': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'AppGtn.entityvehicle': {
            'Meta': {'object_name': 'EntityVehicle'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['AppGtn.VehicleBrand']"}),
            'bridge_number': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'color': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['AppGtn.VehicleColor']"}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'country_of_origin': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['AppGtn.Country']"}),
            'created_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_of_issue_psm': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'deleted_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'engine_number': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifided_date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'number_psm': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '6', 'blank': 'True'}),
            'serial_number': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'serial_psm': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'transmission_number': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'year_of_issue': ('django.db.models.fields.PositiveSmallIntegerField', [], {'max_length': '4'})
        },
        u'AppGtn.kindvehicle': {
            'Meta': {'object_name': 'KindVehicle'},
            'code': ('django.db.models.fields.PositiveSmallIntegerField', [], {'unique': 'True', 'max_length': '3'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'created_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifided_date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'AppGtn.manufacturer': {
            'Meta': {'object_name': 'Manufacturer'},
            'addr': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['AppGtn.Country']"}),
            'created_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifided_date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '300'})
        },
        u'AppGtn.organizationissue': {
            'Meta': {'object_name': 'OrganizationIssue'},
            'addr': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'created_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifided_date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '300'})
        },
        u'AppGtn.typeandgroupvehicle': {
            'Meta': {'object_name': 'TypeAndGroupVehicle'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'created_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveSmallIntegerField', [], {'max_length': '1'}),
            'modifided_date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'parent_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'AppGtn.typeprop': {
            'Meta': {'object_name': 'TypeProp'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'created_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifided_date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'AppGtn.vehiclebrand': {
            'Meta': {'object_name': 'VehicleBrand'},
            'brand_category': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'brand_engine': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['AppGtn.VehicleEngine']", 'symmetrical': 'False', 'blank': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'created_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'heigth': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind_vihicle': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['AppGtn.KindVehicle']"}),
            'length': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'manufacturer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['AppGtn.Manufacturer']"}),
            'max_speed': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'modifided_date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'sertificate_data': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'sertificate_number': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'sirtificate_issue': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['AppGtn.OrganizationIssue']", 'blank': 'True'}),
            'type_brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['AppGtn.TypeAndGroupVehicle']"}),
            'type_prop': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['AppGtn.TypeProp']"}),
            'weight': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'width': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'})
        },
        u'AppGtn.vehiclecolor': {
            'Meta': {'object_name': 'VehicleColor'},
            'color_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'created_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifided_date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'AppGtn.vehicleengine': {
            'Meta': {'object_name': 'VehicleEngine'},
            'brand_engine': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['AppGtn.BrandEngine']"}),
            'brand_vehicle': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['AppGtn.VehicleBrand']", 'symmetrical': 'False', 'blank': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'created_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifided_date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'power_hp': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'power_kwt': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'type_engine': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'working_voluem': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '10'})
        }
    }

    complete_apps = ['AppGtn']