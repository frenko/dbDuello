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

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .forms import OperaForm, AttachForm
from .models import Opera, Attach

def index(request):
    all_operas = Opera.objects.values()
    header_page = _('Home Page:')
    context = {'request': request,
                'all_operas': all_operas, 'header_page': header_page}
    return render(request, 'webapp/home.html', context)
    
def log_in(request):
	header_page = _('Login:')
	context = {'header_page': header_page}
	if request.method == 'POST':
		usern = request.POST['username']
		passwd = request.POST['password']
		
		user = authenticate(username=usern, password=passwd)
		if user is not None:
			login(request, user)
			return HttpResponseRedirect(reverse('webapp:index'))
		else:
			return HttpResponseRedirect(reverse('webapp:login'))
	else:
		
		return render(request, 'webapp/login.html', context);

@login_required
def log_out(request):
	logout(request)
	return HttpResponseRedirect(reverse('webapp:index'))

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

def view_opera(request, opera_id):
	opera = get_object_or_404(Opera, pk=opera_id)
	
	if opera.title and opera.author:
		header_page = string_concat(opera.title, ' <small>', opera.author, '</small>')
	elif not opera.title:
		if opera.author:
			header_page = string_concat(_('Opera ID: '), opera.id, ' <small>', opera.author, '</small>')
		else:
			header_page = string_concat(_('Opera ID: '), opera.id)
	elif not opera.author:
		header_page = string_concat(opera.title, ' <small>', _('Unknown Author'), '</small>')
			
	n_attach = len(opera.media.all())

	if n_attach > 0:
		attachments = opera.media.all()
	else:
		attachments = None

	context = {'opera': opera, 'attachments': attachments, 
				'n_attach': n_attach, 'header_page': header_page}
	return render(request, 'webapp/details.html', context)        

@login_required
def mod_opera(request, opera_id):
	
	modif = True
	
	opera = get_object_or_404(Opera, pk=opera_id)
	
	header_page = _('Modify Opera ID: ') + opera.id
	
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
				'opera_id': opera_id, 'modif': modif, 
				'header_page': header_page}
		
		return render(request, 'webapp/modify.html', context)

@login_required
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
    
    header_page = string_concat(_('All Operas'), ' | ', _('Page: '), str(operas.number))
                   
    return render(request, 'webapp/allopera.html', 
                {'operas': operas, 'header_page': header_page})

def latest(request):
    latest_opera_list = Opera.objects.order_by('-pub_date')[:15]
    header_page = _('Latest Opera')
    context = {'latest_opera_list': latest_opera_list, 
			'header_page': header_page}
    return render(request, 'webapp/latest.html', context)
    
@login_required
def user_profile(request, user_id):
	
	user = User.objects.get(pk=user_id)
	
	header_page = string_concat(_('User: '), user.username)
	
	context = {'header_page': header_page}
	
	return render(request, 'webapp/admin/user.html', context)
