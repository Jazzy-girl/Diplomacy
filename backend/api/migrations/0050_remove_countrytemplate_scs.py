# Generated by Django 5.2.1 on 2025-06-25 13:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0049_territorytemplate_home_center'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='countrytemplate',
            name='scs',
        ),
    ]
