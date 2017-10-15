# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class ufHistory(models.Model):
    publishedDate = models.DateField(unique=True)
    ufValue = models.FloatField(default = -1)
    
    def __str__(self):
        return str(self.publishedDate) + ", " + str(self.ufValue)

