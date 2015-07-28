from django.db import models

class Event(models.Model):
    headline = models.TextField(default='')
