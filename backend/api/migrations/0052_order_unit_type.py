# Generated by Django 5.2.1 on 2025-06-27 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0051_rename_winter_order_order_adjustment_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='unit_type',
            field=models.CharField(choices=[('A', 'Army'), ('F', 'Fleet')], default=None, max_length=1),
            preserve_default=False,
        ),
    ]
