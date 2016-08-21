from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Attach(models.Model):
    file_upload = models.FileField(_('Attachment'), upload_to='documents')
    file_name = models.CharField(_('File Name'), max_length=100)
    file_type = models.CharField(_('File Type'), max_length=100)
    file_size = models.CharField(_('File Size'), max_length=100)
    notes = models.CharField(_('Notes'), max_length=100)
    
    def __str__(self):
        return self.file_name

class Opera(models.Model):
    title = models.CharField(_('Title'), max_length=100)
    title_original = models.CharField(_('Original Title'), max_length=100)
    author = models.CharField(_('Author'), max_length=100)
    period = models.CharField(_('Period'), max_length=100)
    location = models.CharField(_('Location'), max_length=100)
    writing_date = models.PositiveSmallIntegerField(_('Writing Date'))
    description = models.TextField(_('Description'))
    quote = models.TextField(_('Quote'))
    quote_original = models.TextField(_('Original Quote'))
    media = models.ManyToManyField(Attach, related_name="operas")
    pub_date = models.DateTimeField(_('Published Date'), auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)        
        
        
        
        
        
