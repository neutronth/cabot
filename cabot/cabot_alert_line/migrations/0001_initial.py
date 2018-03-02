# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-02-26 10:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cabotapp', '0006_auto_20170821_1000'),
    ]

    operations = [
        migrations.CreateModel(
            name='LineAlert',
            fields=[
                ('alertplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='cabotapp.AlertPlugin')),
            ],
            options={
                'abstract': False,
            },
            bases=('cabotapp.alertplugin',),
        ),
        migrations.CreateModel(
            name='LineAlertUserData',
            fields=[
                ('alertpluginuserdata_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='cabotapp.AlertPluginUserData')),
                ('line_alias', models.CharField(blank=True, max_length=50)),
            ],
            options={
                'abstract': False,
            },
            bases=('cabotapp.alertpluginuserdata',),
        ),
    ]