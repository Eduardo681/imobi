from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from innerpages.models import Immobile, City, Visits


@login_required(login_url='/auth/logar/')
def home(request) -> HttpResponse:
    min_value = request.GET.get('min')
    max_value = request.GET.get('max')
    city = request.GET.get('city')
    types = request.GET.getlist('type')
    cities = City.objects.all()
    if min_value or max_value or city or types:
        if not min_value:
            min_value = 0
        if not max_value:
            max_value = 99999999999999999
        if not types:
            types = ['A', 'H']

        immobiles = Immobile.objects \
            .filter(value__gte=min_value) \
            .filter(value__lte=max_value) \
            .filter(type_immobile__in=types)

        if int(city) != 0:
            immobiles = immobiles.filter(city=city)

    else:
        immobiles = Immobile.objects.all()

    return render(request, 'home.html', {'immobiles': immobiles, 'cities': cities})


def immobile(request, id):
    immobiles = get_object_or_404(Immobile, id=id)
    hint = Immobile.objects.filter(city=immobiles.city).exclude(id=id)[:2]
    return render(request, 'immobile.html', {'immobile': immobiles, 'hints': hint, 'id': id})


def schedule(request):
    user = request.user
    day = request.POST.get('day')
    time = request.POST.get('time')
    id_immobile = request.POST.get('id_immobile')

    visits = Visits(
        immobile_id=id_immobile,
        user=user,
        day=day,
        time=time,
        status='S'
    )
    visits.save()

    return redirect('/schedules')


def schedules(request):
    visits = Visits.objects.filter(user=request.user)
    return render(request, "schedules.html", {'visits': visits})


def cancel(request, id):
    visitas = get_object_or_404(Visits, id=id)
    visitas.status = "C"
    visitas.save()
    return redirect('/schedules')
