from django.shortcuts import get_object_or_404, render

from .models import Opera

def index(request):
    latest_opera_list = Opera.objects.order_by('-pub_date')[:5]
    context = {'latest_opera_list': latest_opera_list}
    return render(request, 'webapp/index.html', context)

def view_opera(request, opera_id):
    retrieved_opera = get_object_or_404(Opera, pk=opera_id)
    return render(request, 'webapp/view.html', {'retrieved_opera': retrieved_opera})
