# Generated by Django 3.2.6 on 2021-11-02 10:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0003_auto_20211102_0823'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bill',
            old_name='radiology_service',
            new_name='radiology_request',
        ),
    ]