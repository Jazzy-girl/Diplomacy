# Generated by Django 5.2.1 on 2025-06-22 21:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0043_alter_order_turn'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnitRetreatOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('turn', models.PositiveSmallIntegerField()),
                ('game', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.game')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.order')),
                ('sandbox', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.sandbox')),
                ('territory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.territory')),
            ],
        ),
    ]
