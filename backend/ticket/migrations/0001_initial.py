# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('grade', models.PositiveIntegerField()),
                ('no', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TicketApplication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=4)),
                ('schoolID', models.CharField(max_length=6)),
                ('societyID', models.CharField(max_length=18)),
                ('requirement', models.PositiveIntegerField()),
                ('organization', models.ForeignKey(to='ticket.Organization')),
            ],
        ),
    ]
