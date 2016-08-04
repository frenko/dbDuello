from __future__ import unicode_literals
from django.db import models
from django.forms import ModelForm
from django.core.validators import MinLengthValidator
from django.core.validators import MaxLengthValidator

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
    media_data = models.TextField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class OperaForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(OperaForm, self).__init__(*args, **kwargs)
        self.fields['writing_date'].max_length = 4
        self.fields['writing_date'].min_length = 4
        self.fields['writing_date'].validators.append(MinLengthValidator)
        self.fields['writing_date'].validators.append(MaxLengthValidator)
    
    class Meta:
        model = Opera
        fields = ['title', 'title_original', 'author', 'period',
                'location', 'writing_date', 'description', 'quote',
                'quote_original']
