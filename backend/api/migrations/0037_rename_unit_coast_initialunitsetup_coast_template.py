# Generated by Django 5.2.1 on 2025-06-17 21:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0036_remove_territorytemplate_unit_coast_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='initialunitsetup',
            old_name='unit_coast',
            new_name='coast_template',
        ),
    ]
