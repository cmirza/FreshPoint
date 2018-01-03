from django.shortcuts import render
from .local_variables import goog_api_key
from .models import Season, State, Vegetable
from datetime import datetime
import calendar
import requests


def index(request):
    return render(request, 'freshpoint/index.html')


def results(request):

    # get users zip code
    user_zip = request.POST['input_zip']

    # pass users zip code to Google Geocode, get JSON response, get users state name
    api_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(user_zip, goog_api_key))
    api_response_dict = api_response.json()
    for i in api_response_dict['results'][0]['address_components']:
        if i['types'] == ["administrative_area_level_1", "political"]:
            user_state = i['short_name']
            user_state_verbose = api_response_dict['results'][0]['formatted_address']

    # get current month id, add leading zero
    current_year = datetime.now().year
    current_month = datetime.now().month
    current_day = datetime.now().day
    days_in_month = calendar.monthrange(current_year, current_month)[1]
    if current_day < days_in_month/2:
        month_id = current_month*2-1
    else:
        month_id = current_month*2
    month_id = format(month_id, '02d')

    # get state object from from model
    user_state = State.objects.get(state_name=user_state)

    # filter season data by users state and users month id
    user_veg = Season.objects.filter(seasons_state=user_state, seasons__icontains=month_id)

    # create list of relevant vegetables from vegetable model
    user_veg_detail = []
    for i in user_veg:
        user_veg_detail.append(Vegetable.objects.get(veg_name=i.seasons_veg))

    context = {'user_state_verbose': user_state_verbose, 'user_veg_detail': user_veg_detail}

    return render(request, 'freshpoint/results.html', context)


def detail(request, url_key):

    veg_detail = Vegetable.objects.get(id=url_key)
    context = {'veg_detail': veg_detail}

    return render(request, 'freshpoint/detail.html', context)