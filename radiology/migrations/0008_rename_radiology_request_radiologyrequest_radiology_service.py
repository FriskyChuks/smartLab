# Generated by Django 3.2.6 on 2021-11-02 10:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('radiology', '0007_rename_radiology_service_radiologyrequest_radiology_request'),
    ]

    operations = [
        migrations.RenameField(
            model_name='radiologyrequest',
            old_name='radiology_request',
            new_name='radiology_service',
        ),
    ]
