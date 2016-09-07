import tempfile
import os

from utils import sizeof_fmt, get_latest_opera
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


def index(request):
    """Return a rendered index page of dbDuello"""
    all_operas = Opera.objects.values()
    header_page = _('Home Page')
    context = {'request': request,
               'all_operas': all_operas,
               'header_page': header_page}
    return render(request, 'webapp/home.html', context)


def view_opera(request, opera_id):
        """
        View opera

        keyword arguments:
        opera_id -- database id of the requested opera

        return:
        rendered page of opera
        """
        opera = get_object_or_404(Opera, pk=opera_id)
        n_attach = 0

        if opera.title and opera.author:
                header_page = string_concat(opera.title,
                                            ' <small>',
                                            opera.author, '</small>')
        elif not opera.title:
                if opera.author:
                        header_page = string_concat(_('Opera ID: '),
                                                    opera.id, ' <small>',
                                                    opera.author, '</small>')
                else:
                        header_page = string_concat(_('Opera ID: '), opera.id)
        elif not opera.author:
                header_page = string_concat(opera.title,
                                            ' <small>',
                                            _('Unknown Author'),
                                            '</small>')

        n_attach = len(opera.media.all())

        if n_attach > 0:
                attachments = opera.media.all()
        else:
                attachments = None

        context = {'opera': opera, 'attachments': attachments,
                   'n_attach': n_attach,
                   'header_page': header_page}
        return render(request, 'webapp/details.html', context)


def allopera(request):
    """
    List opera

    Retrive all operas in database and perform a pagination

    Return a rendered page of all operas
    """
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

    header_page = string_concat(_('All Operas'), ' | ', _('Page: '),
                                str(operas.number))
    title_page = _('All Operas')

    context = {'operas': operas, 'header_page': header_page,
               'title_page': title_page, 'pagination': pagination}
    return render(request, 'webapp/listoperas.html', context)


def latest(request):
    """
    Latest Opera

    Return latest operas added in the database
    """
    #~ latest_opera_list = Opera.objects.order_by('-pub_date')[:15]
    latest_opera_list = get_latest_opera(15)

    header_page = _('Recently added Operas')
    title_page = _('Recently')
    pagination = False

    context = {'operas': latest_opera_list,
               'header_page': header_page, 'title_page': title_page,
               'pagination': pagination}
    return render(request, 'webapp/listoperas.html', context)


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

    header_page = string_concat(_('All Operas'),
                                ' | ', _('Page: '), str(operas.number))
    title_page = _('All Operas')

    context = {'operas': operas, 'header_page': header_page,
               'title_page': title_page, 'pagination': pagination}
    return render(request, 'webapp/users/lists.html', context)


@login_required
def mod_opera(request, opera_id):
        """
        Modify Opera

        keyword arguments:
        opera_id -- database id of requested opera to modify

        return:
        rendered page with form for permit the update of opera
        """
        modif = True

        opera = get_object_or_404(Opera, pk=opera_id)

        header_page = string_concat(_('Modify Opera ID: '), opera.id)

        if request.method == 'POST':
                opera_form = OperaForm(request.POST)

                if opera_form.is_valid():
                        operaValid = opera_form.save(commit=False)
                        operaValid.id = opera_id
                        operaValid.save()
                        return HttpResponseRedirect(
                                        reverse('webapp:view_opera',
                                                args=(opera_id,)))
        else:
                opera_form = OperaForm(instance=opera)

                context = {'opera_form': opera_form,
                           'opera_id': opera_id, 'modif': modif,
                           'header_page': header_page}

                return render(request, 'webapp/modify.html', context)


@login_required
def delete(request, opera_id):
        """
        Detele opera

        keyword arguments:
        opera_id -- database id of requested opera to delete
        """
        opera = get_object_or_404(Opera, pk=opera_id)
        opera.delete()
        return True


@login_required
@permission_required('webapp.add_opera', raise_exception=True)
def add(request):
    """
    Expose add page with form and store a data from form in a database
    """
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
            return HttpResponseRedirect(reverse('webapp:view_opera',
                                                args=(opera_id,)))

    else:
        attach_forms = AttachForm()
        opera_forms = OperaForm()

        context = {'opera_forms': opera_forms,
                   'attach_forms': attach_forms,
                   'header_page': header_page}
        return render(request, 'webapp/add.html', context)


@login_required
def user_profile(request):
    n_opera = Opera.objects.count()
    n_attach = Attach.objects.count()

    latest = get_latest_opera(5)

    context = {'n_opera': n_opera, 'n_attach': n_attach,
               'latest': latest}
    return render(request, 'webapp/users/profile.html', context)
