# Generated by Django 5.2.1 on 2025-06-17 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0029_country_country_template'),
    ]

    operations = [
        migrations.RenameField(
            model_name='territorytemplate',
            old_name='country',
            new_name='country_template',
        ),
        migrations.AddField(
            model_name='territorytemplate',
            name='unit_type',
            field=models.CharField(blank=True, choices=[('A', 'Army'), ('F', 'Fleet')], default=None, max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='unit',
            name='type',
            field=models.CharField(choices=[('A', 'Army'), ('F', 'Fleet')], max_length=1),
        ),
    ]
