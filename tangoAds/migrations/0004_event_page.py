# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tangoAds', '0003_page'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='page',
            field=models.ForeignKey(default=None, to='tangoAds.Page'),
        ),
    ]
