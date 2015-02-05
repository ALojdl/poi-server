# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoursquareChildCategories',
            fields=[
                ('id', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('pluralName', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('shortName', models.CharField(max_length=20)),
                ('parentId', models.CharField(max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FoursquareGrandchildCategories',
            fields=[
                ('id', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('pluralName', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('shortName', models.CharField(max_length=20)),
                ('parentId', models.CharField(max_length=20)),
                ('grandparentId', models.CharField(max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FoursquareMainCategories',
            fields=[
                ('id', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('pluralName', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('shortName', models.CharField(max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
