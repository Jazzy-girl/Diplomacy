# Generated by Django 5.2.1 on 2025-07-06 15:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0056_alter_order_fail_reason_alter_order_origin_territory_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CountrySCCountSnapshot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scs', models.PositiveSmallIntegerField()),
                ('turn', models.PositiveSmallIntegerField()),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.country')),
                ('game', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.game')),
                ('sandbox', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.sandbox')),
            ],
        ),
        migrations.CreateModel(
            name='TerritoryCountrySnapshot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('turn', models.PositiveSmallIntegerField()),
                ('country', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.country')),
                ('game', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.game')),
                ('sandbox', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.sandbox')),
                ('territory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.territory')),
            ],
        ),
    ]
