from __future__ import unicode_literals

from django.db import models

class Opera(models.Model):
    title = models.CharField(max_length=100)
    title_original = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    period = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    writing_date = models.DateField()
    description = models.TextField()
    quote = models.TextField()
    quote_original = models.TextField()
    media_data = models.TextField()
    pub_date = models.DateTimeField('date published')
    
    def __str__(self):
        return self.title
    
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
