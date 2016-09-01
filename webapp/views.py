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
from .userviews import *

def index(request):
    all_operas = Opera.objects.values()
    header_page = _('Home Page')
    context = {'request': request,
                'all_operas': all_operas, 'header_page': header_page}
    return render(request, 'webapp/home.html', context)

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
	
	header_page = string_concat(_('Modify Opera ID: '), opera.id)
	
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
    return render(request, 'webapp/listoperas.html', context)

def latest(request):
    latest_opera_list = Opera.objects.order_by('-pub_date')[:15]
    
    header_page = _('Recently added Operas')
    title_page = _('Recently')
    pagination = False
    
    context = {'operas': latest_opera_list, 
			'header_page': header_page, 'title_page': title_page, 
			'pagination': pagination}
    return render(request, 'webapp/listoperas.html', context)
