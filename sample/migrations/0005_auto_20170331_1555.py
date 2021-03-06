# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-31 13:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sample', '0004_auto_20170331_1540'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
                ('institution', models.CharField(max_length=1000)),
            ],
        ),
        migrations.AddField(
            model_name='sampleset',
            name='final_report',
            field=models.FileField(null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='sampleset',
            name='number_of_samples',
            field=models.PositiveSmallIntegerField(default=0, editable=False),
        ),
        migrations.AddField(
            model_name='sampleset',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sample.Client'),
        ),
    ]
