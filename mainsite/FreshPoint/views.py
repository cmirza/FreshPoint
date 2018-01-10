from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .local_variables import goog_api_key
from .models import Season, State, Vegetable
from datetime import datetime
import calendar
import requests
import re
import json


def index(request):
    return render(request, 'freshpoint/index.html')


def results(request):

    # get users zip code
    user_zip = request.GET['user_zip']

    # pass users zip code to Google Geocode, get JSON response, get users state name
    api_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?components=country:US|postal_code:{0}&key={1}'.format(user_zip, goog_api_key))
    api_response_dict = api_response.json()

    # if zip code fails regex or fails Google Geocode, render error page
    if re.match(r'^(?![0-9]{5}$)', user_zip) or api_response_dict['status'] == 'ZERO_RESULTS':
        message = 'Invalid Zip Code.'
        error = {'message': message}
        return JsonResponse(error)

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

    # create list for vegetable results and list for user state in verbose and abbreviated format
    user_veg_result = []
    user_state_result = [str(user_state_verbose), str(user_state)]

    # iterate over user veg query set and get vegetable object
    for i in user_veg:
        veg_object = Vegetable.objects.get(veg_name=i.seasons_veg)

        # check if vegetable is about to go out of season and create an alert
        season_array = i.seasons[1:-1]
        season_array = season_array.split(",")
        season_array = map(int, season_array)
        if int(month_id)+1 in season_array:
            alert = ''
        else:
            alert = 'Almost Out Of Season!'

        # append user_veg_dict with vegetable
        user_veg_result.append([veg_object.id, veg_object.veg_name, veg_object.veg_image, alert])

    # create dict for JSON output and return output
    output = {'state': user_state_result, 'vegetable': user_veg_result}
    return JsonResponse(output)


def detail(request):

    # get requested vegetable
    vegetable = request.GET['vegetable']

    # use url key to get vegetable object from model, add to context dict
    veg_detail = Vegetable.objects.get(id=vegetable)

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
    veg_seasons = Season.objects.filter(seasons_veg=vegetable)

    # for each states seasons, if current season is seasons, add that state to current states list
    for i in veg_seasons:
        if current_season in i.seasons:
            current_states.append([str(i.seasons_state)])

    # create
    output = {'vegetable': [veg_detail.veg_name, veg_detail.veg_image, veg_detail.veg_desc], 'current_states': [current_states]}
    return JsonResponse(output)
