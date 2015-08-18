from django.db import models

class Page(models.Model):
    pass

class Event(models.Model):
    headline = models.TextField(default='')
    page = models.ForeignKey(Page, default=None)
    