# Generated by Django 5.2.1 on 2025-06-17 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0030_rename_country_territorytemplate_country_template_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='countrytemplate',
            name='scs',
            field=models.PositiveSmallIntegerField(default=3),
        ),
    ]
