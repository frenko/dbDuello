from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Attach(models.Model):
    file_upload = models.FileField(_('Attachment'), 
								upload_to='documents', blank=True)
    file_name = models.CharField(_('File Name'), max_length=200,
								blank=True)
    file_type = models.CharField(_('File Type'), max_length=100,
								blank=True)
    file_size = models.IntegerField(_('File Size'), blank=True)
    notes = models.CharField(_('Notes'), max_length=100, blank=True)
    
    def __str__(self):
        return self.file_name

class Opera(models.Model):
    title = models.CharField(_('Title'), max_length=100, blank=True)
    title_original = models.CharField(_('Original Title'), 
									max_length=100, blank=True)
    author = models.CharField(_('Author'), max_length=100, blank=True)
    period = models.CharField(_('Period'), max_length=100, blank=True)
    location = models.CharField(_('Location'), max_length=100,
								blank=True)
    writing_date = models.PositiveSmallIntegerField(_('Writing Date'), 
													default=0)
    description = models.TextField(_('Description'), blank=True)
    quote = models.TextField(_('Quote'), blank=True)
    quote_original = models.TextField(_('Original Quote'), blank=True)
    media = models.ManyToManyField(Attach, related_name="operas")
    pub_date = models.DateTimeField(_('Published Date'), 
								auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)        
        
        
        
        
        
