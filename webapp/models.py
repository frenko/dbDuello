from __future__ import unicode_literals
from django.db import models

class Attach(models.Model):
    file_upload = models.FileField(upload_to='documents')
    file_name = models.CharField(max_length=100)
    file_type = models.CharField(max_length=100)
    file_size = models.CharField(max_length=100)
    notes = models.CharField(max_length=100)
    
    def __str__(self):
        return self.file_name

class Opera(models.Model):
    title = models.CharField(max_length=100)
    title_original = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    period = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    writing_date = models.PositiveSmallIntegerField()
    description = models.TextField()
    quote = models.TextField()
    quote_original = models.TextField()
    media = models.ManyToManyField(Attach, related_name="operas")
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)        
        
        
        
        
        
