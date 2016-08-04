from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from .models import Opera, OperaForm

def index(request):
    all_operas = Opera.objects.values()
    context = {'request': request,
                'all_operas': all_operas}
    return render(request, 'webapp/home.html', context)
    
def add(request):
    '''
    Expose add page with form and store a data from form in na database
    '''
    if request.method == 'POST':
        forms = OperaForm(request.POST)
        if forms.is_valid():    
            addedOpera = forms.save()
            opera_id = addedOpera.id
            return HttpResponseRedirect(reverse('webapp:view_opera', args=(opera_id,)))
        #else:
            #context forms.errors()
    else:
        forms = OperaForm()
        context = {'forms': forms}
        return render(request, 'webapp/add.html', context)
        
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

def view_opera(request, opera_id):
    opera = get_object_or_404(Opera, pk=opera_id)
    return render(request, 'webapp/details.html', {'opera': opera})
