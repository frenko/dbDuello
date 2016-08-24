import tempfile
import os

from utils import sizeof_fmt
from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from .forms import OperaForm, AttachForm
from .models import Opera, Attach

def index(request):
    all_operas = Opera.objects.values()
    context = {'request': request,
                'all_operas': all_operas}
    return render(request, 'webapp/home.html', context)
    
def login(request):
	return render(request, 'webapp/login.html');

def add(request):
    '''
    Expose add page with form and store a data from form in na database
    '''
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
                'attach_forms': attach_forms}
        return render(request, 'webapp/add.html', context)

def view_opera(request, opera_id):
    opera = get_object_or_404(Opera, pk=opera_id)
    
    n_attach = len(opera.media.all())
    
    if n_attach > 0:
        attachments = opera.media.all()
    else:
        attachments = None
    
    context = {'opera': opera, 'attachments': attachments, 'n_attach': n_attach}
    return render(request, 'webapp/details.html', context)        

def mod_opera(request, opera_id):
	
	modif = True
	
	opera = get_object_or_404(Opera, pk=opera_id)
	
	if request.method == 'POST':
		opera_form = OperaForm(request.POST)
		
		if opera_form.is_valid():
			operaValid = opera_form.save(commit=False)
			operaValid.id = opera_id
			operaValid.save()
			return HttpResponseRedirect(reverse('webapp:view_opera', args=(opera_id,)))
	else:
		opera_form = OperaForm(instance=opera)
		
		context = {'opera_form': opera_form, 
				'opera_id': opera_id, 'modif': modif}
		
		return render(request, 'webapp/modify.html', context)

def delete(request, opera_id):
	opera = get_object_or_404(Opera, pk=opera_id)
	opera.delete()
	return True
	
        
def allopera(request):
    allOpera = Opera.objects.all()
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
               
    return render(request, 'webapp/allopera.html', 
                {'operas': operas})

def latest(request):
    latest_opera_list = Opera.objects.order_by('-pub_date')[:15]
    context = {'latest_opera_list': latest_opera_list}
    return render(request, 'webapp/latest.html', context)
