from django.shortcuts import render

from .models import Division


def division_index(request):
    context = {}
    context['divisions'] = Division.objects.all()

    return render(request, 'core/division_index.html', context=context)


def division_detail(request, slug):
    context = {}
    context['division'] = Division.objects.get(slug=slug)

    return render(request, 'core/division_detail.html', context=context)
