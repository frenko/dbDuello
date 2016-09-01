import tempfile
import os

from utils import sizeof_fmt
from django.conf import settings
from django.utils.translation import string_concat
from django.utils.translation import ugettext_lazy as _

from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .forms import OperaForm, AttachForm
from .models import Opera, Attach

@login_required
@permission_required('webapp.add_opera', raise_exception=True)
def add(request):
    '''
    Expose add page with form and store a data from form in na database
    '''
    
    header_page = _('Add Opera')
    if request.method == 'POST':
        opera_forms = OperaForm(request.POST)
        attach_forms = AttachForm(request.POST, request.FILES)
        
        if request.FILES:
            uploadedFile = request.FILES['file_upload']        
            file_name = os.path.splitext(uploadedFile.name)[0]        
            file_size = uploadedFile.size        
            file_type = uploadedFile.content_type
            
            if attach_forms.is_valid():
                addeddAttach = attach_forms.save(commit=False)
                
                addeddAttach.file_name = file_name
                addeddAttach.file_size = file_size
                addeddAttach.file_type = file_type
                            
                addeddAttach.save()
        
        if opera_forms.is_valid():
            addeddOpera = opera_forms.save()
            if request.FILES:
                addeddOpera.media.add(addeddAttach)
            opera_id = addeddOpera.id
            addeddOpera.save()
            return HttpResponseRedirect(reverse('webapp:view_opera', args=(opera_id,)))
    
    else:
        attach_forms = AttachForm()
        opera_forms = OperaForm()
        
        context = {'opera_forms': opera_forms, 
                'attach_forms': attach_forms, 
                'header_page': header_page}
        return render(request, 'webapp/add.html', context)
        
def listopera(request):
    allOpera = Opera.objects.all()
    
    pagination = True
    paginator = Paginator(allOpera, 10)
    page = request.GET.get('page')
    
    try:
        operas = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        operas = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        operas = paginator.page(paginator.num_pages)
    
    header_page = string_concat(_('All Operas'), ' | ', _('Page: '), str(operas.number))
    title_page = _('All Operas')
    
    context = {'operas': operas, 'header_page': header_page, 
			'title_page': title_page, 'pagination': pagination}
    return render(request, 'webapp/users/lists.html', context)

@login_required
def user_profile(request, user_id):
	
	user = User.objects.get(pk=user_id)
	
	header_page = string_concat(_('User: '), user.username)
	
	context = {'header_page': header_page}
	
	return render(request, 'webapp/users/profile.html', context)
