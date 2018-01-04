from django.shortcuts import render
from .local_variables import goog_api_key
from .models import Season, State, Vegetable
from datetime import datetime
import calendar
import requests
import re


def index(request):
    return render(request, 'freshpoint/index.html')


def results(request):

    # get users zip code
    user_zip = request.POST['input_zip']

    # pass users zip code to Google Geocode, get JSON response, get users state name
    api_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?components=country:US|postal_code:{0}&key={1}'.format(user_zip, goog_api_key))
    api_response_dict = api_response.json()

    # if zip code fails regex or fails Google Geocode, render error page
    if re.match(r'^(?![0-9]{5}$)', user_zip) or api_response_dict['status'] == 'ZERO_RESULTS':
        message = 'Invalid Zip Code.'
        context = {'message': message}
        return render(request, 'freshpoint/error.html', context)

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

    # create list for user veg results and alerts results. for each item item in user results, add vegetable object to
    # user results, turn stringified array into an array of ints, if the next month is in the list create blank entry
    # in list, otherwise create an alert. then zip the two lists together
    user_veg_results = []
    veg_results_alert = []
    for i in user_veg:
        user_veg_results.append(Vegetable.objects.get(veg_name=i.seasons_veg))
        season_array = i.seasons[1:-1]
        season_array = season_array.split(",")
        season_array = map(int, season_array)
        if int(month_id)+1 in season_array:
            veg_results_alert.append('')
        else:
            veg_results_alert.append('Almost Out Of Season!')
    user_veg_results = zip(user_veg_results, veg_results_alert)
    print(veg_results_alert)

    context = {'user_state_verbose': user_state_verbose, 'user_veg_results': user_veg_results}

    return render(request, 'freshpoint/results.html', context)


def detail(request, url_key):

    # use url key to get vegetable object from model, add to context dict
    veg_detail = Vegetable.objects.get(id=url_key)

    # get current season id, add leading zero, make it a string
    current_year = datetime.now().year
    current_month = datetime.now().month
    current_day = datetime.now().day
    days_in_month = calendar.monthrange(current_year, current_month)[1]
    if current_day < days_in_month/2:
        month_id = current_month*2-1
    else:
        month_id = current_month*2
    current_season = str(format(month_id, '02d'))

    # create a list for current states, create query set for seasons containing current vegetable
    current_states = [['State']]
    veg_seasons = Season.objects.filter(seasons_veg=url_key)

    # for each states seasons, if current season is seasons, add that state to current states list
    for i in veg_seasons:
        if current_season in i.seasons:
            current_states.append([str(i.seasons_state)])

    context = {'veg_detail': veg_detail, 'current_states': current_states}

    return render(request, 'freshpoint/detail.html', context)