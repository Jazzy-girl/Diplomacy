# Generated by Django 5.2.1 on 2025-05-22 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_rename_supported_territory_order_other_territory_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='other_territory',
            field=models.CharField(blank=True, default=None, max_length=20, null=True),
        ),
    ]
