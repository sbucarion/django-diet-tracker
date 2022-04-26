from django.shortcuts import render, redirect
from .forms import LogForm
from .models import Log
from django.db.models import Q
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

from django.utils import timezone
from datetime import datetime, timedelta, date
from dateutil.tz import tzutc, tzlocal


@login_required(login_url='/login/')
def index(request):
    form = LogForm()

    #Check if the info is being submitted or just viewed
    if request.method == 'POST':
        form = LogForm(request.POST)

        #Make sure data being submitted is the same as the database
        if form.is_valid():

            instance = form.save(commit=False)
            instance.user = request.user
            instance.calorie = instance.calorie * instance.quantity
            instance.protein = instance.protein * instance.quantity
            instance.fats = instance.fats * instance.quantity
            instance.carbs = instance.carbs * instance.quantity

            #Send to database
            instance.save()
            return redirect("/tracker")

    context = {'form': form}
    return render(request, "tracker.html", context)


@login_required(login_url='/login/')
def display(request):
    #Dates used for filtering rows
    today = date.today()
    tomorrow = today + timedelta(days=1)

    #Query log rows with today and tomorrows since UTC is standard time
    data = Log.objects.filter(Q(time_created__contains=today) | Q(time_created__contains=tomorrow))

    #Loop over queried rows
    ids = []
    for object in data:
        #Covert row UTC time to local time
        utc_time = (object.time_created)
        local_time = utc_time.astimezone(tzlocal())

        #Filter for entries with only local time date
        if str(today)[:10] == str(local_time)[:10]:
            ids.append(int(object.id))

    #Remove columns from query that do not contain dietary info
    clean_data = Log.objects.filter(user=request.user, pk__in=ids).aggregate(Sum('calorie'), Sum('protein'), Sum('fats'), Sum('carbs'))

    #Convert query to dictionary to send to html form
    dict_ = {'Calories': clean_data['calorie__sum'],'Protein': clean_data['protein__sum'], 'Fats': clean_data['fats__sum'], 'Carbs': clean_data['carbs__sum']}

    return render(request, "display.html", {'data': dict_})