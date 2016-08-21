from django.forms import ModelForm
from .models import Opera, Attach
from django.core.validators import MinLengthValidator
from django.core.validators import MaxLengthValidator

class OperaForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(OperaForm, self).__init__(*args, **kwargs)
        self.fields['writing_date'].max_length = 4
        self.fields['writing_date'].min_length = 4
        self.fields['writing_date'].validators.append(MinLengthValidator)
        self.fields['writing_date'].validators.append(MaxLengthValidator)
    
    class Meta:
        model = Opera
        exclude = ['media', 'pub_date']

class AttachForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(AttachForm, self).__init__(*args, **kwargs)
        
    class Meta:
        model = Attach
        exclude = ['file_size', 'file_type', 'file_name']
